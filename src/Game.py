"""The game itself"""

import tkinter as tk
from types import TracebackType
from tkinter import Event
from typing import Callable
from random import random, choice
import Grid
from Utils import Directions


class Game:
    """Game class where all the magic happens"""

    def __init__(self) -> None:
        self.grid: Grid.Grid = Grid.Grid()
        self.root: tk.Tk = tk.Tk()
        self.root.title("2048")
        self.mainframe: tk.Frame = tk.Frame(self.root)
        self._setMainframe()

        self.is_root_alive: bool = True
        self.root.bind_all("<Key>", self._key)
        self._directions: list[str] = [el.name for el in Directions]
        self._dir_func: dict[str, Callable[[], bool]] = {
            direction: function
            for direction, function in zip(
                self._directions, [self.grid.up, self.grid.left, self.grid.down, self.grid.right]
            )
        }

        self._newTile()
        self.grid.updateAvailableSpace()
        self.grid.draw()

    def _setMainframe(self) -> None:
        self.mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S)
        tk.Label(
            self.mainframe,
            text="Test",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=0, row=0)
        tk.Label(
            self.mainframe,
            text="Test2",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=1, row=0)
        tk.Label(
            self.mainframe,
            text="Test3",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=2, row=0)
        tk.Label(
            self.mainframe,
            text="Test4",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=0, row=1)
        tk.Label(
            self.mainframe,
            text="Test5",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=1, row=1)
        tk.Label(
            self.mainframe,
            text="Test6",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=2, row=1)
        tk.Label(
            self.mainframe,
            text="Test7",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=0, row=2)
        tk.Label(
            self.mainframe,
            text="Test8",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=1, row=2)
        tk.Label(
            self.mainframe,
            text="Test9",
            foreground="black",
            background="red",
            width=10,
            height=5,
        ).grid(column=2, row=2)

    def __enter__(self) -> "Game":
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.is_root_alive:
            self.root.destroy()

    def _destroy(self) -> None:
        self.is_root_alive = False
        self.root.destroy()

    def _key(self, event: Event) -> None:
        key: str = event.keysym
        moved: bool = False
        match key:
            case "Escape":
                self._destroy()
            case val if val in self._directions:
                while self._dir_func[val]():
                    moved = True
            case _:
                pass

        if self._isEndgame():
            self._destroy()

        if moved:
            self._newTile()
        self.grid.draw()

    def _isEndgame(self) -> bool:
        if any(2048 in row for row in self.grid.grid):
            return True
        if any(0 in row for row in self.grid.grid):
            return False
        for y in range(self.grid.size):
            for x in range(self.grid.size):
                if self.grid.inside(x + 1, y):
                    if self.grid[y][x + 1] == self.grid[y][x]:
                        return False
                if self.grid.inside(x, y + 1):
                    if self.grid[y + 1][x] == self.grid[y][x]:
                        return False
        return True

    def _newTile(self) -> None:
        if not self.grid.available_space:
            return

        empty_cells: list[tuple[int, int]] = []
        for y in range(self.grid.size):
            for x in range(self.grid.size):
                if self.grid.grid[y][x] == 0:
                    empty_cells.append((x, y))
        if not empty_cells:
            return
        x, y = choice(empty_cells)
        self.grid.grid[y][x] = 2 if random() < 0.8 else 4
