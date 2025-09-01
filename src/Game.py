"""The game itself"""

import tkinter as tk
from types import TracebackType
from tkinter import Event
from typing import Callable
from random import random, choice
import Grid
from Utils import Directions, hsl2rgb


class Game:
    """Game class where all the magic happens"""

    def __init__(self) -> None:
        self.grid: Grid.Grid = Grid.Grid()
        self.window: tk.Tk = tk.Tk()
        self.window.title("2048")
        self.mainframe: tk.Frame = tk.Frame(self.window)
        self._setMainframe()
        self.gui_grid: list[list[tk.Label]]
        self._colors: dict[int, str]

        self.is_root_alive: bool = True
        self.window.bind_all("<Key>", self._key)
        self._directions: list[str] = [el.name for el in Directions]
        self._dir_func: dict[str, Callable[[], bool]] = {
            direction: function
            for direction, function in zip(
                self._directions, [self.grid.up, self.grid.left, self.grid.down, self.grid.right]
            )
        }
        self._win = 2048

        self._colors = self._generateColors(0, 100, 66.4)

        self._newTile()
        self.grid.updateAvailableSpace()
        self._draw()

    def _setMainframe(self) -> None:
        self.mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S)
        self.gui_grid = self._generateTiles()

    def _generateTiles(self) -> list[list[tk.Label]]:
        width = 10
        tiles: list[list[tk.Label]] = [[] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                tile = tk.Label(
                    self.mainframe,
                    text="",
                    foreground="black",
                    background="white",
                    width=width,
                    height=width // 2,
                    highlightbackground="black",
                    highlightthickness=1,
                    font=("Arial", 20, "bold"),
                )
                tile.grid(row=i, column=j)
                tiles[i].append(tile)
        return tiles

    def _generateColors(self, hue: int, start_lightness: float, end_lightness: float) -> dict[int, str]:
        keys: list[int] = [0, 2]
        while keys[-1] < self._win:
            keys.append(keys[-1] * 2)
        steps: int = len(keys) - 1
        delta: float = (end_lightness - start_lightness) / steps

        colors: dict[int, str] = {}
        for i, key in enumerate(keys):
            lightness = start_lightness + delta * i
            colors[key] = hsl2rgb(hue, 100, lightness)
        return colors

    def __enter__(self) -> "Game":
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.is_root_alive:
            self.window.destroy()

    def _destroy(self) -> None:
        self.is_root_alive = False
        self.window.destroy()

    def _key(self, event: Event) -> None:
        key: str = event.keysym
        moved: bool = False
        match key:
            case "Escape":
                self._destroy()
                return
            case val if val in self._directions:
                while self._dir_func[val]():
                    moved = True
            case _:
                pass

        if self._isEndgame():
            self._destroy()

        if moved:
            self._newTile()
        self._draw()

    def _isEndgame(self) -> bool:
        if any(self._win in row for row in self.grid.grid):
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

    def _draw(self) -> None:
        for i in range(4):
            for j in range(4):
                value: int = self.grid.grid[i][j]
                self.gui_grid[i][j].config(text=("" if value == 0 else str(value)), background=self._colors[value])
