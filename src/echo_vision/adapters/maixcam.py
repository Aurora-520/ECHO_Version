from __future__ import annotations

import importlib.util
import time

from echo_vision.core import FaultFlag, Frame, HealthSnapshot, HealthState
from echo_vision.ports import CameraSource, CameraSourceError


class MaixCamCameraSource(CameraSource):
    """V0 boundary for MaixCAM; implementation waits for confirmed device API."""

    def __init__(self) -> None:
        self._started = False
        self._message = "MaixCAM adapter is deferred until firmware and camera API are discovered"

    @staticmethod
    def runtime_available() -> bool:
        return importlib.util.find_spec("maix") is not None

    def start(self) -> None:
        if not self.runtime_available():
            raise CameraSourceError("maix runtime is not available on this host")
        raise CameraSourceError(self._message)

    def read(self, timeout_s: float | None = None) -> Frame | None:
        del timeout_s
        raise CameraSourceError("MaixCAM source is not started")

    def stop(self) -> None:
        self._started = False

    def health(self) -> HealthSnapshot:
        return HealthSnapshot(
            schema_version=1,
            state=HealthState.UNKNOWN,
            monotonic_ns=time.monotonic_ns(),
            fault_flags=FaultFlag.CAMERA_UNAVAILABLE,
            message=self._message,
        )
