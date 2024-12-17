import unittest
from geometry.vector import Vector
import math


class TestVector(unittest.TestCase):

    def test_addition(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        self.assertEqual(v1 + v2, Vector(4, 6))

    def test_subtraction(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        self.assertEqual(v1 - v2, Vector(-2, -2))

    def test_multiplication(self):
        v = Vector(1, 2)
        self.assertEqual(v * 3, Vector(3, 6))

    def test_rmultiplication(self):
        v = Vector(1, 2)
        self.assertEqual(3 * v, Vector(3, 6))

    def test_division(self):
        v = Vector(6, 8)
        self.assertEqual(v / 2, Vector(3, 4))

    def test_negation(self):
        v = Vector(1, 2)
        self.assertEqual(-v, Vector(-1, -2))

    def test_equality(self):
        v1 = Vector(1, 2)
        v2 = Vector(1, 2)
        v3 = Vector(3, 4)
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)

    def test_str(self):
        v = Vector(1, 2)
        self.assertEqual(str(v), "(x: 1, y: 2)")

    def test_normalize(self):
        v = Vector(3, 4)
        self.assertEqual(v.normalize(), Vector(0.6, 0.8))

    def test_length(self):
        v = Vector(3, 4)
        self.assertEqual(v.length(), 5)

    def test_to_tuple(self):
        v = Vector(1, 2)
        self.assertEqual(v.to_tuple(), (1, 2))


if __name__ == '__main__':
    unittest.main()