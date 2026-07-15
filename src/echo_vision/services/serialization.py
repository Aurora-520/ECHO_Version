from __future__ import annotations

from enum import IntEnum, IntFlag
from typing import Any

from echo_vision.core import Detection, HealthSnapshot, Track, VisionResult


def _normalize(value: Any) -> Any:
    if isinstance(value, (IntEnum, IntFlag)):
        return int(value)
    if isinstance(value, tuple):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize(item) for key, item in value.items()}
    return value


def _detection_to_dict(detection: Detection) -> dict[str, Any]:
    return {
        "target_class": int(detection.target_class),
        "confidence": detection.confidence,
        "coordinate_frame": int(detection.coordinate_frame),
        "x": detection.x,
        "y": detection.y,
        "bbox_xywh": None if detection.bbox_xywh is None else list(detection.bbox_xywh),
        "attributes": _normalize(dict(detection.attributes)),
    }


def _track_to_dict(track: Track) -> dict[str, Any]:
    return {
        "track_id": track.track_id,
        "detection": _detection_to_dict(track.detection),
        "velocity_x_per_s": track.velocity_x_per_s,
        "velocity_y_per_s": track.velocity_y_per_s,
        "age_frames": track.age_frames,
        "missed_frames": track.missed_frames,
    }


def result_to_dict(result: VisionResult) -> dict[str, Any]:
    return {
        "schema_version": result.schema_version,
        "sequence": result.sequence,
        "frame_id": result.frame_id,
        "mode": int(result.mode),
        "captured_monotonic_ns": result.captured_monotonic_ns,
        "produced_monotonic_ns": result.produced_monotonic_ns,
        "valid": result.valid,
        "target_class": int(result.target_class),
        "coordinate_frame": int(result.coordinate_frame),
        "x": result.x,
        "y": result.y,
        "confidence": result.confidence,
        "fault_flags": int(result.fault_flags),
        "detections": [_detection_to_dict(item) for item in result.detections],
        "track": None if result.track is None else _track_to_dict(result.track),
    }


def health_to_dict(health: HealthSnapshot) -> dict[str, Any]:
    return {
        "schema_version": health.schema_version,
        "state": int(health.state),
        "monotonic_ns": health.monotonic_ns,
        "fps": health.fps,
        "latency_p50_ms": health.latency_p50_ms,
        "latency_p95_ms": health.latency_p95_ms,
        "dropped_frames": health.dropped_frames,
        "queue_high_water": health.queue_high_water,
        "result_age_ms": health.result_age_ms,
        "memory_used_bytes": health.memory_used_bytes,
        "temperature_c": health.temperature_c,
        "fault_flags": int(health.fault_flags),
        "message": health.message,
    }
