from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, IntFlag
from types import MappingProxyType
from typing import Any, Mapping

import numpy as np


class PixelFormat(IntEnum):
    GRAY8 = 1
    RGB8 = 2
    BGR8 = 3


class CoordinateFrame(IntEnum):
    UNKNOWN = 0
    IMAGE_PX = 1
    IMAGE_NORM = 2
    ERROR_PX = 3
    CAMERA_RAY = 4
    PLANE_MM = 5


class TargetClass(IntEnum):
    UNKNOWN = 0
    LIGHT_SPOT = 1
    LINE = 2
    CIRCLE = 3
    RECTANGLE = 4
    BOARD_CELL = 5
    GAME_PIECE = 6
    PARKING_SLOT = 7
    MOVING_TARGET = 8


class VisionMode(IntEnum):
    IDLE = 0
    GEOMETRY = 1
    LINE_FOLLOW = 2
    AIM = 3
    BOARD = 4
    PARKING = 5
    TRACKING = 6


class HealthState(IntEnum):
    UNKNOWN = 0
    OK = 1
    DEGRADED = 2
    FAULT = 3


class FaultFlag(IntFlag):
    NONE = 0
    CAMERA_UNAVAILABLE = 1 << 0
    FRAME_STALE = 1 << 1
    LOW_CONFIDENCE = 1 << 2
    PIPELINE_ERROR = 1 << 3
    COMM_LOST = 1 << 4
    CONFIG_INVALID = 1 << 5
    MODEL_MISSING = 1 << 6
    RECORDER_DROPPED = 1 << 7


@dataclass(frozen=True, slots=True)
class Frame:
    frame_id: int
    captured_monotonic_ns: int
    source: str
    pixel_format: PixelFormat
    image: np.ndarray = field(repr=False, compare=False)
    metadata: Mapping[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if self.frame_id < 0:
            raise ValueError("frame_id must be non-negative")
        if self.captured_monotonic_ns < 0:
            raise ValueError("captured_monotonic_ns must be non-negative")
        if not isinstance(self.image, np.ndarray):
            raise TypeError("image must be a numpy.ndarray")
        if self.image.ndim not in (2, 3):
            raise ValueError("image must have 2 or 3 dimensions")
        if self.image.dtype != np.uint8:
            raise ValueError("image dtype must be uint8")
        if self.image.ndim == 2 and self.pixel_format != PixelFormat.GRAY8:
            raise ValueError("2D images require GRAY8")
        if self.image.ndim == 3 and self.image.shape[2] != 3:
            raise ValueError("color images require exactly 3 channels")
        self.image.setflags(write=False)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    @property
    def width(self) -> int:
        return int(self.image.shape[1])

    @property
    def height(self) -> int:
        return int(self.image.shape[0])


@dataclass(frozen=True, slots=True)
class Detection:
    target_class: TargetClass
    confidence: float
    coordinate_frame: CoordinateFrame
    x: float
    y: float
    bbox_xywh: tuple[float, float, float, float] | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if self.coordinate_frame == CoordinateFrame.UNKNOWN:
            raise ValueError("detection coordinate frame must be explicit")
        if self.bbox_xywh is not None and len(self.bbox_xywh) != 4:
            raise ValueError("bbox_xywh must contain four values")
        object.__setattr__(self, "attributes", MappingProxyType(dict(self.attributes)))


@dataclass(frozen=True, slots=True)
class Track:
    track_id: int
    detection: Detection
    velocity_x_per_s: float = 0.0
    velocity_y_per_s: float = 0.0
    age_frames: int = 1
    missed_frames: int = 0

    def __post_init__(self) -> None:
        if self.track_id < 0:
            raise ValueError("track_id must be non-negative")
        if self.age_frames < 1 or self.missed_frames < 0:
            raise ValueError("track ages must be non-negative")


@dataclass(frozen=True, slots=True)
class VisionResult:
    schema_version: int
    sequence: int
    frame_id: int
    mode: VisionMode
    captured_monotonic_ns: int
    produced_monotonic_ns: int
    valid: bool
    target_class: TargetClass
    coordinate_frame: CoordinateFrame
    x: float
    y: float
    confidence: float
    fault_flags: FaultFlag = FaultFlag.NONE
    detections: tuple[Detection, ...] = ()
    track: Track | None = None

    def __post_init__(self) -> None:
        if self.schema_version < 1:
            raise ValueError("schema_version must be positive")
        if self.sequence < 0 or self.frame_id < 0:
            raise ValueError("sequence and frame_id must be non-negative")
        if self.produced_monotonic_ns < self.captured_monotonic_ns:
            raise ValueError("produced timestamp cannot precede capture")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if self.valid and self.coordinate_frame == CoordinateFrame.UNKNOWN:
            raise ValueError("valid results require an explicit coordinate frame")

    def age_ms(self, now_monotonic_ns: int) -> float:
        return max(0.0, (now_monotonic_ns - self.captured_monotonic_ns) / 1_000_000.0)

    @classmethod
    def invalid(
        cls,
        *,
        sequence: int,
        frame: Frame,
        mode: VisionMode,
        produced_monotonic_ns: int,
        fault_flags: FaultFlag = FaultFlag.NONE,
    ) -> "VisionResult":
        return cls(
            schema_version=1,
            sequence=sequence,
            frame_id=frame.frame_id,
            mode=mode,
            captured_monotonic_ns=frame.captured_monotonic_ns,
            produced_monotonic_ns=produced_monotonic_ns,
            valid=False,
            target_class=TargetClass.UNKNOWN,
            coordinate_frame=CoordinateFrame.UNKNOWN,
            x=0.0,
            y=0.0,
            confidence=0.0,
            fault_flags=fault_flags,
        )


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    schema_version: int
    state: HealthState
    monotonic_ns: int
    fps: float = 0.0
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0
    dropped_frames: int = 0
    queue_high_water: int = 0
    result_age_ms: float = 0.0
    memory_used_bytes: int | None = None
    temperature_c: float | None = None
    fault_flags: FaultFlag = FaultFlag.NONE
    message: str = ""

    def __post_init__(self) -> None:
        if self.schema_version < 1 or self.monotonic_ns < 0:
            raise ValueError("invalid health snapshot version or timestamp")
        if self.dropped_frames < 0 or self.queue_high_water < 0:
            raise ValueError("health counters must be non-negative")
