"""Testing the Grid class"""

import copy
from itertools import repeat
import unittest
from src.Grid import Grid


class TestGridMove(unittest.TestCase):
    """Tests for the move method in the Grid class"""

    def _generateGrid(self) -> list[list[int]]:
        return [[0 for _ in repeat(None, 4)] for _ in repeat(None, 4)]

    def testMoveSingle(self) -> None:
        """Test the move method with a single number"""
        top_right = self._generateGrid()
        top_right[0][3] = 2
        top_left = self._generateGrid()
        top_left[0][0] = 2
        bottom_left = self._generateGrid()
        bottom_left[3][0] = 2
        bottom_right = self._generateGrid()
        bottom_right[3][3] = 2
        top_center = self._generateGrid()
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

    def testMultiplenNumbersPack(self) -> None:
        """Test the move method when there are multiple numbers involved in a pack"""
        top_right = self._generateGrid()
        top_right[0][2:] = [2, 4]
        top_right[1][2:] = [4, 2]
        top_left = self._generateGrid()
        top_left[0][:2] = [2, 4]
        top_left[1][:2] = [4, 2]
        bottom_right = self._generateGrid()
        bottom_right[2][2:] = [2, 4]
        bottom_right[3][2:] = [4, 2]
        bottom_left = self._generateGrid()
        bottom_left[2][:2] = [2, 4]
        bottom_left[3][:2] = [4, 2]

        grid: Grid = Grid()
        grid.grid = top_right
        grid.down()
        self.assertEqual(grid.grid, bottom_right)
        grid.left()
        self.assertEqual(grid.grid, bottom_left)
        grid.up()
        self.assertEqual(grid.grid, top_left)
        grid.right()
        self.assertEqual(grid.grid, top_right)

    def testMultipleNumbersSeparated(self) -> None:
        """Test the move method when there are multiple numbers involded separated"""
        start = self._generateGrid()
        start[0][0] = 2
        start[2][0] = 4
        end = self._generateGrid()
        end[0][0] = 2
        end[1][0] = 4

        grid: Grid = Grid()
        grid.grid = copy.deepcopy(start)
        grid.up()
        self.assertEqual(grid.grid, end)

        end = self._generateGrid()
        end[2][0] = 2
        end[3][0] = 4
        grid.grid = copy.copy(start)
        grid.down()
        self.assertEqual(grid.grid, end)

        start = self._generateGrid()
        start[0][0] = 2
        start[0][2] = 4
        end = self._generateGrid()
        end[0][2] = 2
        end[0][3] = 4

        grid.grid = copy.deepcopy(start)
        grid.right()
        self.assertEqual(grid.grid, end)

        end = self._generateGrid()
        end[0][0] = 2
        end[0][1] = 4

        grid.grid = copy.deepcopy(start)
        grid.left()
        self.assertEqual(grid.grid, end)

    def testSimpleMergings(self) -> None:
        """Test when there are just 2 numbers able to merge"""
        start = self._generateGrid()
        start[0][0] = 2
        start[0][1] = 2
        end = self._generateGrid()
        end[0][0] = 4

        grid: Grid = Grid()
        grid.grid = copy.deepcopy(start)
        grid.left()
        self.assertEqual(grid.grid, end)

        end = self._generateGrid()
        end[0][3] = 4
        grid.grid = copy.deepcopy(start)
        grid.right()
        self.assertEqual(grid.grid, end)

        start = self._generateGrid()
        start[0][0] = 4
        start[1][0] = 4
        end = self._generateGrid()
        end[0][0] = 8
        grid.grid = copy.deepcopy(start)
        grid.up()
        self.assertEqual(grid.grid, end)

        end = self._generateGrid()
        end[3][0] = 8
        grid.grid = copy.deepcopy(start)
        grid.down()
        self.assertEqual(grid.grid, end)

    @unittest.skip("Need to implement")
    def testMultipleMergings(self) -> None:
        """Test when threre are several possible merges"""


class TestGrid(unittest.TestCase):
    """Test the rest of the class methods"""

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
