from __future__ import annotations

import time

from echo_vision.core import Frame, VisionMode, VisionResult


class NoopPipeline:
    """V0 pipeline that proves data flow without claiming a detection."""

    def __init__(self, mode: VisionMode = VisionMode.IDLE) -> None:
        self._mode = mode
        self._sequence = 0

    def process(self, frame: Frame) -> VisionResult:
        result = VisionResult.invalid(
            sequence=self._sequence,
            frame=frame,
            mode=self._mode,
            produced_monotonic_ns=time.monotonic_ns(),
        )
        self._sequence += 1
        return result
