from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import statistics
import time
from typing import Sequence

from echo_vision.adapters import FileImageSource, JsonlResultSink
from echo_vision.config import load_config
from echo_vision.core import PixelFormat
from echo_vision.pipelines import NoopPipeline, Pipeline
from echo_vision.ports import CameraSource, ResultSink


@dataclass(frozen=True, slots=True)
class ReplaySummary:
    frames: int
    failures: int
    failure_messages: tuple[str, ...]
    elapsed_ms: float
    fps: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_max_ms: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _percentile(values: Sequence[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * percentile
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def run_replay(
    source: CameraSource,
    pipeline: Pipeline,
    *,
    sink: ResultSink | None = None,
    max_frames: int = 0,
) -> ReplaySummary:
    latencies_ms: list[float] = []
    frames = 0
    failures = 0
    failure_messages: list[str] = []
    start_ns = time.monotonic_ns()
    source.start()
    try:
        while max_frames == 0 or frames < max_frames:
            frame = source.read()
            if frame is None:
                break
            try:
                result = pipeline.process(frame)
                latency_ms = (
                    result.produced_monotonic_ns - result.captured_monotonic_ns
                ) / 1_000_000.0
                latencies_ms.append(max(0.0, latency_ms))
                if sink is not None:
                    sink.send_result(result)
            except Exception as exc:
                failures += 1
                if len(failure_messages) < 10:
                    failure_messages.append(f"{type(exc).__name__}: {exc}")
            frames += 1
    finally:
        source.stop()
        if sink is not None:
            sink.close()

    elapsed_ns = max(1, time.monotonic_ns() - start_ns)
    elapsed_ms = elapsed_ns / 1_000_000.0
    fps = frames / (elapsed_ns / 1_000_000_000.0)
    return ReplaySummary(
        frames=frames,
        failures=failures,
        failure_messages=tuple(failure_messages),
        elapsed_ms=elapsed_ms,
        fps=fps,
        latency_p50_ms=statistics.median(latencies_ms) if latencies_ms else 0.0,
        latency_p95_ms=_percentile(latencies_ms, 0.95),
        latency_max_ms=max(latencies_ms, default=0.0),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Replay image files through an ECHO_Vision pipeline")
    parser.add_argument("--config", default="configs/default.json")
    parser.add_argument("--local-config")
    parser.add_argument("--input", help="Image file or directory; overrides source.path")
    parser.add_argument("--output", help="JSONL output; overrides replay.output_jsonl")
    parser.add_argument("--max-frames", type=int, help="0 means all input frames")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    config = load_config(args.config, args.local_config)
    input_path = args.input or config.source.path
    output_path = args.output if args.output is not None else config.replay.output_jsonl
    max_frames = args.max_frames if args.max_frames is not None else config.replay.max_frames
    pixel_format = PixelFormat.GRAY8 if config.source.pixel_format == "gray8" else PixelFormat.RGB8

    source = FileImageSource.from_path(
        input_path,
        patterns=config.source.patterns,
        loop=config.source.loop,
        pixel_format=pixel_format,
    )
    sink = JsonlResultSink(output_path) if output_path else None
    summary = run_replay(source, NoopPipeline(), sink=sink, max_frames=max_frames)
    print(json.dumps(summary.to_dict(), ensure_ascii=True, sort_keys=True))
    return 0 if summary.failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
