from __future__ import annotations

from abc import ABC, abstractmethod

from echo_vision.core import Frame, HealthSnapshot


class CameraSourceError(RuntimeError):
    pass


class CameraSource(ABC):
    """Single-owner source of immutable frames."""

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self, timeout_s: float | None = None) -> Frame | None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> HealthSnapshot:
        raise NotImplementedError

    def __enter__(self) -> "CameraSource":
        self.start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:  # type: ignore[no-untyped-def]
        self.stop()
