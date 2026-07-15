from __future__ import annotations

import time
from typing import Any

import numpy as np

from echo_vision.core import FaultFlag, Frame, HealthSnapshot, HealthState, PixelFormat
from echo_vision.ports import CameraSource, CameraSourceError


class OpenCvCameraSource(CameraSource):
    """Generic V4L2/USB camera adapter for Raspberry Pi and host development."""

    def __init__(self, device: int | str = 0, *, width: int | None = None, height: int | None = None) -> None:
        self._device = device
        self._width = width
        self._height = height
        self._capture: Any = None
        self._frame_id = 0
        self._last_error = ""

    def start(self) -> None:
        try:
            import cv2
        except ImportError as exc:
            raise CameraSourceError("OpenCV is required for the Raspberry Pi camera adapter") from exc
        capture = cv2.VideoCapture(self._device)
        if self._width is not None:
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        if self._height is not None:
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
        if not capture.isOpened():
            capture.release()
            raise CameraSourceError(f"cannot open camera device: {self._device}")
        self._capture = capture
        self._frame_id = 0
        self._last_error = ""

    def read(self, timeout_s: float | None = None) -> Frame | None:
        del timeout_s
        if self._capture is None:
            raise CameraSourceError("OpenCV camera source is not started")
        ok, image = self._capture.read()
        if not ok or image is None:
            self._last_error = "camera read failed"
            raise CameraSourceError(self._last_error)
        array = np.ascontiguousarray(image, dtype=np.uint8)
        frame = Frame(
            frame_id=self._frame_id,
            captured_monotonic_ns=time.monotonic_ns(),
            source=f"opencv:{self._device}",
            pixel_format=PixelFormat.BGR8,
            image=array,
        )
        self._frame_id += 1
        return frame

    def stop(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def health(self) -> HealthSnapshot:
        if self._capture is not None and not self._last_error:
            return HealthSnapshot(1, HealthState.OK, time.monotonic_ns())
        return HealthSnapshot(
            1,
            HealthState.FAULT if self._last_error else HealthState.UNKNOWN,
            time.monotonic_ns(),
            fault_flags=FaultFlag.CAMERA_UNAVAILABLE,
            message=self._last_error,
        )
