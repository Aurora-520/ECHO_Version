from __future__ import annotations

import json
from pathlib import Path
from typing import TextIO

from echo_vision.core import HealthSnapshot, VisionResult
from echo_vision.ports import ResultSink
from echo_vision.services.serialization import health_to_dict, result_to_dict


class JsonlResultSink(ResultSink):
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._file: TextIO | None = None

    def _stream(self) -> TextIO:
        if self._file is None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._file = self._path.open("w", encoding="utf-8", newline="\n")
        return self._file

    def send_result(self, result: VisionResult) -> None:
        record = {"record_type": "vision_result", "data": result_to_dict(result)}
        self._stream().write(json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n")

    def send_health(self, health: HealthSnapshot) -> None:
        record = {"record_type": "health", "data": health_to_dict(health)}
        self._stream().write(json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n")

    def close(self) -> None:
        if self._file is not None:
            self._file.flush()
            self._file.close()
            self._file = None
