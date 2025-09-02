"""
File with the different screens of the game
"""

import tkinter as tk
from random import choice, random
import Grid
from Utils import hsl2rgb


class GameScreen(tk.Frame):
    """
    The screen with the game
    """

    def __init__(self, parent: tk.Frame, controller: tk.Tk) -> None:
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid: Grid.Grid = Grid.Grid()
        self.gui_grid: list[list[tk.Label]]
        self._colors: dict[int, str]

        self._win = 2048

        self.gui_grid = self._generateTiles()
        self._colors = self._generateColors(0, 100, 66.4)

        self.newTile()
        self.grid.updateAvailableSpace()
        self.draw()

    def _generateTiles(self) -> list[list[tk.Label]]:
        width = 10
        tiles: list[list[tk.Label]] = [[] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                tile = tk.Label(
                    self,
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

    def isEndgame(self) -> bool:
        """
        Checks if the player has won
        """
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

    def newTile(self) -> None:
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

    def draw(self) -> None:
        for i in range(4):
            for j in range(4):
                value: int = self.grid.grid[i][j]
                self.gui_grid[i][j].config(text=("" if value == 0 else str(value)), background=self._colors[value])
