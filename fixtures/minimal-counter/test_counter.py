import unittest
from counter import increment


class CounterTests(unittest.TestCase):
    def test_increment_and_cap(self):
        self.assertEqual(increment(2, 4), 3)
        self.assertEqual(increment(4, 4), 4)
        self.assertEqual(increment(0, 0), 0)

    def test_reject_invalid_inputs(self):
        for value, limit in [(-1, 2), (3, 2), (0, -1)]:
            with self.assertRaises(ValueError):
                increment(value, limit)
        with self.assertRaises(TypeError):
            increment(True, 2)


if __name__ == '__main__':
    unittest.main()
