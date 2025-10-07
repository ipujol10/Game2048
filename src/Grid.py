"""Module to have the grid and do all the operations"""


class Grid:
    """Grid class"""

    def __init__(self) -> None:
        self.size: int = 4
        self.grid: list[list[int]]
        self._empty_cells: int
        self.available_space: bool
        self.finished: bool

        self.reset()

    def __getitem__(self, key: int) -> list[int]:
        return self.grid[key]

    def _move(self, *, positive: bool, vertical: bool) -> bool:
        """
        Perform the movement updating the grid

        Args:
            positive (bool): if the direction is on the positive axis (right or down)
            vertical (bool): if the direction is vertical (up or down)

        Returns:
            bool: if there has been any moevement
        """
        start: int
        finish: int
        step: int
        if positive:
            start = self.size - 1
            finish = -1
            step = -1
        else:
            start = 0
            finish = self.size
            step = 1

        moved: bool = False
        for i in range(start, finish, step):
            for j in range(start + step, finish, step):
                (x, y) = (i, j) if vertical else (j, i)
                if (number := self.grid[y][x]) != 0:
                    scan: int = y if vertical else x
                    (scan_start, scan_end, scan_step) = (scan + 1, self.size, 1) if positive else (scan - 1, -1, -1)
                    (x2, y2) = (x, scan) if vertical else (scan, y)
                    stp: int = 1 if positive else -1
                    (x3, y3) = (x, scan + stp) if vertical else (scan + stp, y)
                    moved = self._merge(x2, y2, x3, y3) or moved
                    for scan in range(scan_start, scan_end, scan_step):
                        (x2, y2) = (x, scan) if vertical else (scan, y)
                        (x3, y3) = (x, scan + stp) if vertical else (scan + stp, y)
                        if self.grid[y2][x2] == 0 and (
                            self._inLimit(y2 if vertical else x2, positive) or (self.grid[y3][x3] != 0)
                        ):
                            self.grid[y][x] = 0
                            self.grid[y2][x2] = number
                            moved = True
                            break
                    moved = self._merge(x2, y2, x3, y3) or moved
        return moved

    def inside(self, x: int, y: int) -> bool:
        """Is the cell from the coordinates inside the boundaries?"""
        return 0 <= x < self.size and 0 <= y < self.size

    def _inLimit(self, var: int, positive: bool) -> bool:
        return var == self.size - 1 if positive else var == 0

    def up(self) -> bool:
        """Handle when player press up"""
        return self._move(positive=False, vertical=True)

    def down(self) -> bool:
        """Handle when player press down"""
        return self._move(positive=True, vertical=True)

    def right(self) -> bool:
        """Handle when player press right"""
        return self._move(positive=True, vertical=False)

    def left(self) -> bool:
        """Handle when player press left"""
        return self._move(positive=False, vertical=False)

    def updateAvailableSpace(self) -> None:
        """Updates the flag keeping track that there is room to move"""
        self._empty_cells = sum(row.count(0) for row in self.grid)
        self.available_space = self._empty_cells > 0

    def _merge(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        if not self.inside(x2, y2):
            return False
        current: int = self.grid[y1][x1]
        other: int = self.grid[y2][x2]
        if current != other:
            return False
        self.grid[y1][x1] = 0
        self.grid[y2][x2] *= 2
        self._empty_cells += 1
        self.available_space = True
        if current == 2048:
            self.finished = True
        return True

    def reset(self) -> None:
        """Resset board"""
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self._empty_cells = self.size * self.size
        self.available_space = True
        self.finished = False
