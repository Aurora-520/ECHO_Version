from __future__ import annotations

import time
import unittest

import numpy as np

from echo_vision.core import (
    CoordinateFrame,
    Detection,
    Frame,
    PixelFormat,
    TargetClass,
    VisionMode,
    VisionResult,
)
from echo_vision.services import result_to_dict


class CoreTypesTest(unittest.TestCase):
    def test_frame_is_validated_and_read_only(self) -> None:
        image = np.zeros((8, 10, 3), dtype=np.uint8)
        frame = Frame(1, 100, "test", PixelFormat.RGB8, image, {"name": "sample"})

        self.assertEqual(frame.width, 10)
        self.assertEqual(frame.height, 8)
        self.assertFalse(frame.image.flags.writeable)
        with self.assertRaises(ValueError):
            frame.image[0, 0, 0] = 1
        with self.assertRaises(TypeError):
            frame.metadata["new"] = "value"  # type: ignore[index]

    def test_detection_requires_explicit_coordinates(self) -> None:
        detection = Detection(
            target_class=TargetClass.CIRCLE,
            confidence=0.8,
            coordinate_frame=CoordinateFrame.IMAGE_PX,
            x=12.0,
            y=18.0,
        )
        self.assertEqual(detection.target_class, TargetClass.CIRCLE)
        with self.assertRaises(ValueError):
            Detection(TargetClass.CIRCLE, 0.8, CoordinateFrame.UNKNOWN, 0.0, 0.0)

    def test_invalid_result_does_not_use_coordinates_as_fault(self) -> None:
        now = time.monotonic_ns()
        frame = Frame(3, now, "test", PixelFormat.GRAY8, np.zeros((4, 4), dtype=np.uint8))
        result = VisionResult.invalid(
            sequence=9,
            frame=frame,
            mode=VisionMode.IDLE,
            produced_monotonic_ns=now + 1_000_000,
        )

        self.assertFalse(result.valid)
        self.assertEqual(result.coordinate_frame, CoordinateFrame.UNKNOWN)
        self.assertGreaterEqual(result.age_ms(now + 2_000_000), 2.0)

    def test_detection_attributes_serialize_without_mutating_snapshot(self) -> None:
        now = time.monotonic_ns()
        detection = Detection(
            TargetClass.RECTANGLE,
            0.9,
            CoordinateFrame.IMAGE_PX,
            10.0,
            20.0,
            attributes={"corners": [1, 2, 3, 4]},
        )
        result = VisionResult(
            1,
            1,
            1,
            VisionMode.GEOMETRY,
            now,
            now,
            True,
            TargetClass.RECTANGLE,
            CoordinateFrame.IMAGE_PX,
            10.0,
            20.0,
            0.9,
            detections=(detection,),
        )
        serialized = result_to_dict(result)
        self.assertEqual(serialized["detections"][0]["attributes"]["corners"], [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()
