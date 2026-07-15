from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Mapping


class ConfigError(ValueError):
    pass


DEFAULT_PATTERNS = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.npy")


@dataclass(frozen=True, slots=True)
class SourceConfig:
    kind: str = "file"
    path: str = "datasets/demo"
    patterns: tuple[str, ...] = DEFAULT_PATTERNS
    loop: bool = False
    pixel_format: str = "rgb8"


@dataclass(frozen=True, slots=True)
class ReplayConfig:
    max_frames: int = 0
    output_jsonl: str | None = None


@dataclass(frozen=True, slots=True)
class ProtocolConfig:
    version: int = 1
    max_payload_bytes: int = 512


@dataclass(frozen=True, slots=True)
class DebugConfig:
    enabled: bool = False
    host: str = "127.0.0.1"
    port: int = 8765


@dataclass(frozen=True, slots=True)
class AppConfig:
    source: SourceConfig = SourceConfig()
    replay: ReplayConfig = ReplayConfig()
    protocol: ProtocolConfig = ProtocolConfig()
    debug: DebugConfig = DebugConfig()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        text = os.path.expandvars(path.read_text(encoding="utf-8"))
        value = json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot load config {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigError(f"config root must be an object: {path}")
    return value


def _deep_merge(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _section(data: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = data.get(key, {})
    if not isinstance(value, Mapping):
        raise ConfigError(f"{key} must be an object")
    return value


def _build_config(data: Mapping[str, Any]) -> AppConfig:
    allowed = {"source", "replay", "protocol", "debug"}
    unknown = set(data) - allowed
    if unknown:
        raise ConfigError(f"unknown top-level config keys: {sorted(unknown)}")

    source = _section(data, "source")
    replay = _section(data, "replay")
    protocol = _section(data, "protocol")
    debug = _section(data, "debug")

    patterns = source.get("patterns", DEFAULT_PATTERNS)
    if not isinstance(patterns, (list, tuple)) or not all(isinstance(v, str) for v in patterns):
        raise ConfigError("source.patterns must be a list of strings")

    result = AppConfig(
        source=SourceConfig(
            kind=str(source.get("kind", "file")),
            path=str(source.get("path", "datasets/demo")),
            patterns=tuple(patterns),
            loop=bool(source.get("loop", False)),
            pixel_format=str(source.get("pixel_format", "rgb8")),
        ),
        replay=ReplayConfig(
            max_frames=int(replay.get("max_frames", 0)),
            output_jsonl=(
                None if replay.get("output_jsonl") is None else str(replay["output_jsonl"])
            ),
        ),
        protocol=ProtocolConfig(
            version=int(protocol.get("version", 1)),
            max_payload_bytes=int(protocol.get("max_payload_bytes", 512)),
        ),
        debug=DebugConfig(
            enabled=bool(debug.get("enabled", False)),
            host=str(debug.get("host", "127.0.0.1")),
            port=int(debug.get("port", 8765)),
        ),
    )

    if result.source.kind not in {"file", "maixcam", "raspberry_pi"}:
        raise ConfigError(f"unsupported source.kind: {result.source.kind}")
    if result.source.pixel_format not in {"rgb8", "gray8"}:
        raise ConfigError("source.pixel_format must be rgb8 or gray8")
    if result.replay.max_frames < 0:
        raise ConfigError("replay.max_frames must be non-negative")
    if result.protocol.version < 1 or result.protocol.max_payload_bytes < 1:
        raise ConfigError("invalid protocol configuration")
    if not 1 <= result.debug.port <= 65535:
        raise ConfigError("debug.port must be in [1, 65535]")
    return result


def load_config(default_path: str | Path | None = None, override_path: str | Path | None = None) -> AppConfig:
    data: dict[str, Any] = {}
    if default_path is not None:
        data = _read_json(Path(default_path))
    if override_path is not None:
        data = _deep_merge(data, _read_json(Path(override_path)))
    return _build_config(data)
