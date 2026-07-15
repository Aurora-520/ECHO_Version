from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class SlotDiagnostics:
    published: int
    consumed: int
    overwritten: int
    high_water: int


class LatestValueSlot(Generic[T]):
    """Thread-safe capacity-one channel that overwrites stale values."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._value: T | None = None
        self._published = 0
        self._consumed = 0
        self._overwritten = 0
        self._high_water = 0

    def publish(self, value: T) -> None:
        with self._lock:
            if self._value is not None:
                self._overwritten += 1
            self._value = value
            self._published += 1
            self._high_water = 1

    def take_latest(self) -> T | None:
        with self._lock:
            value = self._value
            if value is not None:
                self._value = None
                self._consumed += 1
            return value

    def diagnostics(self) -> SlotDiagnostics:
        with self._lock:
            return SlotDiagnostics(
                published=self._published,
                consumed=self._consumed,
                overwritten=self._overwritten,
                high_water=self._high_water,
            )
