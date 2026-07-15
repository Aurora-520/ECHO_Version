from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import struct


MAGIC = b"\xA5\x5A"
HEADER = struct.Struct("<2sBBHIIBH")
CRC = struct.Struct("<H")
HEADER_SIZE = HEADER.size
CRC_SIZE = CRC.size
DEFAULT_MAX_PAYLOAD = 512


class ProtocolError(ValueError):
    pass


class MessageType(IntEnum):
    SET_MODE = 0x01
    START = 0x02
    STOP = 0x03
    SET_PARAM = 0x04
    PING = 0x05
    RESULT_SNAPSHOT = 0x81
    HEALTH = 0x82
    ACK = 0x83
    PONG = 0x84


@dataclass(frozen=True, slots=True)
class WireFrame:
    version: int
    message_type: MessageType
    sequence: int
    timestamp_ms: int
    mode: int
    flags: int
    payload: bytes


@dataclass(frozen=True, slots=True)
class StreamDiagnostics:
    frames: int
    crc_or_format_errors: int
    discarded_bytes: int


def crc16_ccitt_false(data: bytes, initial: int = 0xFFFF) -> int:
    value = initial
    for byte in data:
        value ^= byte << 8
        for _ in range(8):
            value = ((value << 1) ^ 0x1021) & 0xFFFF if value & 0x8000 else (value << 1) & 0xFFFF
    return value


def encode_frame(frame: WireFrame, *, max_payload: int = DEFAULT_MAX_PAYLOAD) -> bytes:
    payload = bytes(frame.payload)
    if not 1 <= frame.version <= 255:
        raise ProtocolError("version must be in [1, 255]")
    if len(payload) > max_payload:
        raise ProtocolError("payload exceeds configured maximum")
    if not 0 <= frame.sequence <= 0xFFFFFFFF:
        raise ProtocolError("sequence is outside uint32")
    if not 0 <= frame.timestamp_ms <= 0xFFFFFFFF:
        raise ProtocolError("timestamp_ms is outside uint32")
    if not 0 <= frame.mode <= 0xFF or not 0 <= frame.flags <= 0xFFFF:
        raise ProtocolError("mode or flags is outside wire range")
    header = HEADER.pack(
        MAGIC,
        frame.version,
        int(frame.message_type),
        len(payload),
        frame.sequence,
        frame.timestamp_ms,
        frame.mode,
        frame.flags,
    )
    checksum = crc16_ccitt_false(header[2:] + payload)
    return header + payload + CRC.pack(checksum)


def decode_frame(data: bytes, *, max_payload: int = DEFAULT_MAX_PAYLOAD) -> WireFrame:
    if len(data) < HEADER_SIZE + CRC_SIZE:
        raise ProtocolError("frame is shorter than header and CRC")
    magic, version, message_raw, payload_len, sequence, timestamp_ms, mode, flags = HEADER.unpack_from(data)
    if magic != MAGIC:
        raise ProtocolError("invalid frame magic")
    if version == 0:
        raise ProtocolError("protocol version zero is invalid")
    if payload_len > max_payload:
        raise ProtocolError("payload exceeds configured maximum")
    expected_len = HEADER_SIZE + payload_len + CRC_SIZE
    if len(data) != expected_len:
        raise ProtocolError(f"frame length mismatch: expected {expected_len}, got {len(data)}")
    expected_crc = CRC.unpack_from(data, expected_len - CRC_SIZE)[0]
    actual_crc = crc16_ccitt_false(data[2 : expected_len - CRC_SIZE])
    if expected_crc != actual_crc:
        raise ProtocolError("CRC16 mismatch")
    try:
        message_type = MessageType(message_raw)
    except ValueError as exc:
        raise ProtocolError(f"unknown message type: 0x{message_raw:02X}") from exc
    return WireFrame(
        version=version,
        message_type=message_type,
        sequence=sequence,
        timestamp_ms=timestamp_ms,
        mode=mode,
        flags=flags,
        payload=bytes(data[HEADER_SIZE : HEADER_SIZE + payload_len]),
    )


class StreamDecoder:
    """Incremental UART decoder with bounded payload and byte resynchronization."""

    def __init__(self, *, max_payload: int = DEFAULT_MAX_PAYLOAD) -> None:
        self._max_payload = max_payload
        self._buffer = bytearray()
        self._frames = 0
        self._errors = 0
        self._discarded = 0

    def feed(self, data: bytes) -> list[WireFrame]:
        self._buffer.extend(data)
        decoded: list[WireFrame] = []
        while True:
            start = self._buffer.find(MAGIC)
            if start < 0:
                keep = 1 if self._buffer.endswith(MAGIC[:1]) else 0
                discard = len(self._buffer) - keep
                if discard > 0:
                    del self._buffer[:discard]
                    self._discarded += discard
                break
            if start > 0:
                del self._buffer[:start]
                self._discarded += start
            if len(self._buffer) < HEADER_SIZE:
                break
            payload_len = struct.unpack_from("<H", self._buffer, 4)[0]
            if payload_len > self._max_payload:
                del self._buffer[0]
                self._errors += 1
                self._discarded += 1
                continue
            total_len = HEADER_SIZE + payload_len + CRC_SIZE
            if len(self._buffer) < total_len:
                break
            candidate = bytes(self._buffer[:total_len])
            try:
                frame = decode_frame(candidate, max_payload=self._max_payload)
            except ProtocolError:
                del self._buffer[0]
                self._errors += 1
                self._discarded += 1
                continue
            del self._buffer[:total_len]
            decoded.append(frame)
            self._frames += 1
        return decoded

    def diagnostics(self) -> StreamDiagnostics:
        return StreamDiagnostics(self._frames, self._errors, self._discarded)
