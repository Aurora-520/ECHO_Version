from __future__ import annotations

import time
import unittest

import numpy as np

from echo_vision.core import Frame, PixelFormat, VisionMode, VisionResult
from echo_vision.protocol import (
    MessageType,
    ProtocolError,
    StreamDecoder,
    WireFrame,
    decode_frame,
    decode_result_payload,
    encode_frame,
    encode_result_payload,
)


class ProtocolTest(unittest.TestCase):
    def test_wire_frame_round_trip(self) -> None:
        expected = WireFrame(1, MessageType.PING, 42, 1234, int(VisionMode.IDLE), 3, b"abcd")
        encoded = encode_frame(expected)
        decoded = decode_frame(encoded)
        self.assertEqual(decoded, expected)

    def test_bad_crc_is_rejected(self) -> None:
        encoded = bytearray(encode_frame(WireFrame(1, MessageType.STOP, 2, 3, 0, 0, b"")))
        encoded[-1] ^= 0x01
        with self.assertRaises(ProtocolError):
            decode_frame(bytes(encoded))

    def test_stream_decoder_resynchronizes_after_noise_and_bad_frame(self) -> None:
        first = encode_frame(WireFrame(1, MessageType.START, 1, 10, 1, 0, b""))
        bad = bytearray(encode_frame(WireFrame(1, MessageType.STOP, 2, 20, 1, 0, b"")))
        bad[-1] ^= 0x80
        second = encode_frame(WireFrame(1, MessageType.PING, 3, 30, 1, 0, b"xyz"))
        decoder = StreamDecoder()

        frames = []
        stream = b"noise" + first + bytes(bad) + second
        for index in range(0, len(stream), 3):
            frames.extend(decoder.feed(stream[index : index + 3]))

        self.assertEqual([frame.sequence for frame in frames], [1, 3])
        self.assertGreaterEqual(decoder.diagnostics().crc_or_format_errors, 1)
        self.assertGreaterEqual(decoder.diagnostics().discarded_bytes, 5)

    def test_result_payload_keeps_valid_separate_from_coordinates(self) -> None:
        now = time.monotonic_ns()
        frame = Frame(0, now, "test", PixelFormat.GRAY8, np.zeros((2, 2), dtype=np.uint8))
        result = VisionResult.invalid(
            sequence=1,
            frame=frame,
            mode=VisionMode.IDLE,
            produced_monotonic_ns=now + 1000,
        )
        decoded = decode_result_payload(encode_result_payload(result, result_age_ms=12.4))

        self.assertFalse(decoded.valid)
        self.assertEqual(decoded.result_age_ms, 12)


if __name__ == "__main__":
    unittest.main()
