"""Testing the Grid class"""

import unittest
from src.Grid import Grid


class TestGridMove(unittest.TestCase):
    """Tests for the move method in the Grid class"""

    def testMoveSingle(self) -> None:
        """Test the move method with a single number"""
        top_right = [[0 for _ in range(4)] for _ in range(4)]
        top_right[0][3] = 2
        top_left = [[0 for _ in range(4)] for _ in range(4)]
        top_left[0][0] = 2
        bottom_left = [[0 for _ in range(4)] for _ in range(4)]
        bottom_left[3][0] = 2
        bottom_right = [[0 for _ in range(4)] for _ in range(4)]
        bottom_right[3][3] = 2
        top_center = [[0 for _ in range(4)] for _ in range(4)]
        top_center[0][2] = 2

        grid: Grid = Grid()
        grid.grid[2][2] = 2

        grid.up()
        self.assertEqual(grid.grid, top_center)
        grid.up()
        self.assertEqual(grid.grid, top_center)
        grid.right()
        self.assertEqual(grid.grid, top_right)
        grid.right()
        self.assertEqual(grid.grid, top_right)
        grid.down()
        self.assertEqual(grid.grid, bottom_right)
        grid.down()
        self.assertEqual(grid.grid, bottom_right)
        grid.left()
        self.assertEqual(grid.grid, bottom_left)
        grid.left()
        self.assertEqual(grid.grid, bottom_left)
        grid.up()
        self.assertEqual(grid.grid, top_left)
        grid.up()
        self.assertEqual(grid.grid, top_left)
        grid.right()
        self.assertEqual(grid.grid, top_right)
        grid.right()
        self.assertEqual(grid.grid, top_right)

    def testIsInside(self) -> None:
        """Test the is the coordinate inside the boundaries method"""
        grid: Grid = Grid()

        self.assertTrue(grid.inside(0, 0))
        self.assertTrue(grid.inside(0, 3))
        self.assertTrue(grid.inside(3, 3))
        self.assertTrue(grid.inside(3, 0))
        self.assertTrue(grid.inside(2, 1))

        self.assertFalse(grid.inside(-1, 0))
        self.assertFalse(grid.inside(4, 0))
        self.assertFalse(grid.inside(0, -1))
        self.assertFalse(grid.inside(0, 4))


if __name__ == "__main__":
    unittest.main()
