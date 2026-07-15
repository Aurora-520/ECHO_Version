from __future__ import annotations

from pathlib import Path
import time
from typing import Iterable

import numpy as np
from PIL import Image

from echo_vision.core import (
    FaultFlag,
    Frame,
    HealthSnapshot,
    HealthState,
    PixelFormat,
)
from echo_vision.ports import CameraSource, CameraSourceError


class FileImageSource(CameraSource):
    """Finite file-backed source for deterministic offline replay."""

    def __init__(
        self,
        paths: Iterable[str | Path],
        *,
        loop: bool = False,
        pixel_format: PixelFormat = PixelFormat.RGB8,
        source_name: str = "file",
    ) -> None:
        self._paths = tuple(Path(path) for path in paths)
        if not self._paths:
            raise CameraSourceError("file source has no input images")
        self._loop = loop
        self._pixel_format = pixel_format
        self._source_name = source_name
        self._index = 0
        self._frame_id = 0
        self._started = False
        self._last_error = ""

    @classmethod
    def from_path(
        cls,
        path: str | Path,
        *,
        patterns: Iterable[str] = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.npy"),
        loop: bool = False,
        pixel_format: PixelFormat = PixelFormat.RGB8,
    ) -> "FileImageSource":
        root = Path(path)
        if root.is_file():
            paths = [root]
        elif root.is_dir():
            unique: dict[str, Path] = {}
            for pattern in patterns:
                for candidate in root.glob(pattern):
                    if candidate.is_file():
                        unique[str(candidate.resolve()).lower()] = candidate
            paths = sorted(unique.values(), key=lambda value: value.name.lower())
        else:
            raise CameraSourceError(f"input path does not exist: {root}")
        return cls(paths, loop=loop, pixel_format=pixel_format, source_name=str(root))

    def start(self) -> None:
        self._index = 0
        self._frame_id = 0
        self._last_error = ""
        self._started = True

    def _decode(self, path: Path) -> np.ndarray:
        try:
            if path.suffix.lower() == ".npy":
                array = np.load(path, allow_pickle=False)
                if array.dtype != np.uint8:
                    raise CameraSourceError(f"npy image must use uint8: {path}")
                if self._pixel_format == PixelFormat.GRAY8 and array.ndim == 3:
                    array = np.asarray(Image.fromarray(array).convert("L"))
                elif self._pixel_format == PixelFormat.RGB8 and array.ndim == 2:
                    array = np.asarray(Image.fromarray(array).convert("RGB"))
            else:
                with Image.open(path) as image:
                    mode = "L" if self._pixel_format == PixelFormat.GRAY8 else "RGB"
                    array = np.asarray(image.convert(mode))
            return np.ascontiguousarray(array, dtype=np.uint8)
        except (OSError, ValueError) as exc:
            raise CameraSourceError(f"cannot decode image {path}: {exc}") from exc

    def read(self, timeout_s: float | None = None) -> Frame | None:
        del timeout_s
        if not self._started:
            raise CameraSourceError("file source is not started")
        if self._index >= len(self._paths):
            if not self._loop:
                return None
            self._index = 0

        path = self._paths[self._index]
        frame_id = self._frame_id
        self._index += 1
        self._frame_id += 1
        try:
            image = self._decode(path)
        except CameraSourceError as exc:
            self._last_error = str(exc)
            raise
        return Frame(
            frame_id=frame_id,
            captured_monotonic_ns=time.monotonic_ns(),
            source=self._source_name,
            pixel_format=self._pixel_format,
            image=image,
            metadata={"source_path": str(path.resolve())},
        )

    def stop(self) -> None:
        self._started = False

    def health(self) -> HealthSnapshot:
        state = HealthState.OK if self._started and not self._last_error else HealthState.UNKNOWN
        flags = FaultFlag.NONE
        if self._last_error:
            state = HealthState.FAULT
            flags = FaultFlag.CAMERA_UNAVAILABLE
        return HealthSnapshot(
            schema_version=1,
            state=state,
            monotonic_ns=time.monotonic_ns(),
            fault_flags=flags,
            message=self._last_error,
        )
