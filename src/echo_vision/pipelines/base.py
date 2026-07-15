from __future__ import annotations

from typing import Protocol

from echo_vision.core import Frame, VisionResult


class Pipeline(Protocol):
    def process(self, frame: Frame) -> VisionResult:
        ...
