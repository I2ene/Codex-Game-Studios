"""Actual parent-added tests for the three stated fixture acceptance criteria."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from counter import increment


class AcceptanceTests(unittest.TestCase):
    def test_exact_story_examples(self):
        self.assertEqual(increment(2, 5), 3)
        self.assertEqual(increment(5, 5), 5)
        self.assertEqual(increment(0, 0), 0)

    def test_all_invalid_type_positions(self):
        for value, limit in [(True, 5), (0, True), (1.5, 5), (0, '5')]:
            with self.subTest(value=value, limit=limit), self.assertRaises(TypeError):
                increment(value, limit)
