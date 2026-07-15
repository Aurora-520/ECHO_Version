from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from echo_vision.config import ConfigError, load_config


class ConfigTest(unittest.TestCase):
    def test_default_and_override_merge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            default_path = root / "default.json"
            override_path = root / "override.json"
            default_path.write_text(
                json.dumps({"source": {"path": "a", "loop": False}, "debug": {"port": 8765}}),
                encoding="utf-8",
            )
            override_path.write_text(
                json.dumps({"source": {"path": "b"}, "debug": {"enabled": True}}),
                encoding="utf-8",
            )

            config = load_config(default_path, override_path)

        self.assertEqual(config.source.path, "b")
        self.assertFalse(config.source.loop)
        self.assertTrue(config.debug.enabled)
        self.assertEqual(config.debug.port, 8765)

    def test_unknown_top_level_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"unexpected": true}', encoding="utf-8")
            with self.assertRaises(ConfigError):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
