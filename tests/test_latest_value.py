from __future__ import annotations

import unittest

from echo_vision.services import LatestValueSlot


class LatestValueSlotTest(unittest.TestCase):
    def test_stale_value_is_overwritten_and_counted(self) -> None:
        slot: LatestValueSlot[int] = LatestValueSlot()
        slot.publish(1)
        slot.publish(2)

        self.assertEqual(slot.take_latest(), 2)
        self.assertIsNone(slot.take_latest())
        diagnostics = slot.diagnostics()
        self.assertEqual(diagnostics.published, 2)
        self.assertEqual(diagnostics.consumed, 1)
        self.assertEqual(diagnostics.overwritten, 1)
        self.assertEqual(diagnostics.high_water, 1)


if __name__ == "__main__":
    unittest.main()
