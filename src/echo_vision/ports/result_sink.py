from __future__ import annotations

from abc import ABC, abstractmethod

from echo_vision.core import HealthSnapshot, VisionResult


class ResultSink(ABC):
    """Single-owner output for results and health snapshots."""

    @abstractmethod
    def send_result(self, result: VisionResult) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_health(self, health: HealthSnapshot) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
