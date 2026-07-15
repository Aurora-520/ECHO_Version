from __future__ import annotations

from dataclasses import dataclass
import struct

from echo_vision.core import CoordinateFrame, FaultFlag, TargetClass, VisionResult
from echo_vision.protocol.framing import ProtocolError


RESULT_PAYLOAD = struct.Struct("<BBBBfffHI")


@dataclass(frozen=True, slots=True)
class ResultPayload:
    valid: bool
    target_class: TargetClass
    coordinate_frame: CoordinateFrame
    x: float
    y: float
    confidence: float
    result_age_ms: int
    fault_flags: FaultFlag


def encode_result_payload(result: VisionResult, *, result_age_ms: float) -> bytes:
    age = max(0, min(0xFFFF, round(result_age_ms)))
    return RESULT_PAYLOAD.pack(
        1 if result.valid else 0,
        int(result.target_class),
        int(result.coordinate_frame),
        0,
        float(result.x),
        float(result.y),
        float(result.confidence),
        age,
        int(result.fault_flags),
    )


def decode_result_payload(payload: bytes) -> ResultPayload:
    if len(payload) != RESULT_PAYLOAD.size:
        raise ProtocolError(
            f"result payload length mismatch: expected {RESULT_PAYLOAD.size}, got {len(payload)}"
        )
    valid, target_raw, coordinate_raw, reserved, x, y, confidence, age_ms, flags = RESULT_PAYLOAD.unpack(payload)
    if reserved != 0:
        raise ProtocolError("result payload reserved byte must be zero")
    if valid not in (0, 1):
        raise ProtocolError("result valid field must be zero or one")
    if not 0.0 <= confidence <= 1.0:
        raise ProtocolError("result confidence is outside [0, 1]")
    try:
        target_class = TargetClass(target_raw)
        coordinate_frame = CoordinateFrame(coordinate_raw)
    except ValueError as exc:
        raise ProtocolError("unknown target class or coordinate frame") from exc
    if valid and coordinate_frame == CoordinateFrame.UNKNOWN:
        raise ProtocolError("valid result cannot use UNKNOWN coordinates")
    return ResultPayload(
        valid=bool(valid),
        target_class=target_class,
        coordinate_frame=coordinate_frame,
        x=x,
        y=y,
        confidence=confidence,
        result_age_ms=age_ms,
        fault_flags=FaultFlag(flags),
    )
