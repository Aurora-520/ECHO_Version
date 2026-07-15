from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from echo_vision.adapters import FileImageSource, JsonlResultSink
from echo_vision.core import PixelFormat
from echo_vision.pipelines import NoopPipeline
from echo_vision.runtime import run_replay


class FileReplayTest(unittest.TestCase):
    def test_file_source_and_jsonl_replay(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            Image.new("RGB", (16, 12), (255, 0, 0)).save(root / "a.png")
            Image.new("RGB", (16, 12), (0, 255, 0)).save(root / "b.png")
            output = root / "results.jsonl"

            source = FileImageSource.from_path(root, pixel_format=PixelFormat.RGB8)
            summary = run_replay(source, NoopPipeline(), sink=JsonlResultSink(output))

            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(summary.frames, 2)
        self.assertEqual(summary.failures, 0)
        self.assertEqual(summary.failure_messages, ())
        self.assertGreater(summary.fps, 0.0)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["record_type"], "vision_result")
        self.assertFalse(records[0]["data"]["valid"])

    def test_empty_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(RuntimeError):
                FileImageSource.from_path(directory)

    def test_looping_source_keeps_monotonic_frame_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            Image.new("L", (2, 2), 0).save(root / "one.png")
            source = FileImageSource.from_path(root, loop=True, pixel_format=PixelFormat.GRAY8)
            source.start()
            try:
                ids = [source.read().frame_id for _ in range(3)]  # type: ignore[union-attr]
            finally:
                source.stop()
        self.assertEqual(ids, [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
