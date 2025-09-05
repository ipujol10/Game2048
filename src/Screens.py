"""
File with the different screens of the game
"""

import tkinter as tk
from tkinter import Event
from typing import Callable, TYPE_CHECKING
from random import choice, random
from abc import ABC, abstractmethod
import Grid
from Utils import hsl2rgb, Directions

if TYPE_CHECKING:
    from Game import Game


class MyScreen(ABC, tk.Frame):
    """Interface for Screens"""

    def __init__(self, parent: tk.Frame) -> None:
        tk.Frame.__init__(self, master=parent)

    @abstractmethod
    def bindKeyboard(self) -> None:
        """
        Bind the current screen keys
        """


class GameScreen(MyScreen):
    """
    The screen with the game
    """

    def __init__(self, parent: tk.Frame, controller: "Game") -> None:
        MyScreen.__init__(self, parent)
        self.controller = controller

        self.matrix: Grid.Grid = Grid.Grid()
        self.gui_grid: list[list[tk.Label]]
        self._colors: dict[int, str]

        self.bind_all("<Key>", self._key)
        self._directions: list[str] = [el.name for el in Directions]
        self._dir_func: dict[str, Callable[[], bool]] = {
            direction: function
            for direction, function in zip(
                self._directions, [self.matrix.up, self.matrix.left, self.matrix.down, self.matrix.right]
            )
        }

        self._win = 2048

        self.gui_grid = self._generateTiles()
        self._colors = self._generateColors(165, 100, 66.4)

        self.reset()

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
        if any(self._win in row for row in self.matrix.grid):
            return True
        if any(0 in row for row in self.matrix.grid):
            return False
        for y in range(self.matrix.size):
            for x in range(self.matrix.size):
                if self.matrix.inside(x + 1, y):
                    if self.matrix[y][x + 1] == self.matrix[y][x]:
                        return False
                if self.matrix.inside(x, y + 1):
                    if self.matrix[y + 1][x] == self.matrix[y][x]:
                        return False
        return True

    def newTile(self) -> None:
        """
        Generate a new tile if there is space
        """
        if not self.matrix.available_space:
            return

        empty_cells: list[tuple[int, int]] = []
        for y in range(self.matrix.size):
            for x in range(self.matrix.size):
                if self.matrix.grid[y][x] == 0:
                    empty_cells.append((x, y))
        if not empty_cells:
            return
        x, y = choice(empty_cells)
        self.matrix.grid[y][x] = 2 if random() < 0.8 else 4

    def draw(self) -> None:
        """
        Refresh the state of the game
        """
        for i in range(4):
            for j in range(4):
                value: int = self.matrix.grid[i][j]
                self.gui_grid[i][j].config(text=("" if value == 0 else str(value)), background=self._colors[value])

    def _key(self, event: Event) -> None:
        key: str = event.keysym
        moved: bool = False
        match key:
            case "Escape":
                self.controller.showScreen("MainMenuScreen")
                return
            case val if val in self._directions:
                while self._dir_func[val]():
                    moved = True
            case _:
                pass

        if self.isEndgame():
            self.reset()
            self.controller.showScreen("MainMenuScreen")
            return

        if moved:
            self.newTile()
        self.draw()

    def bindKeyboard(self) -> None:
        """
        Bind the current screen keys
        """
        self.unbind_all("<Key>")
        self.bind_all("<Key>", self._key)

    def reset(self) -> None:
        """Reset the game"""
        self.matrix.reset()
        self.newTile()
        self.matrix.updateAvailableSpace()
        self.draw()


class MainMenuScreen(MyScreen):
    """
    Main Menu screen class
    """

    def __init__(self, parent: tk.Frame, controller: "Game") -> None:
        MyScreen.__init__(self, parent)
        self.controller = controller

        tk.Button(
            self,
            text="New Game",
            command=self._newGameButtonBind,
            font=("Arial", 20),
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Continue Game",
            command=self._continueGameButtonBind,
            font=("Arial", 20),
        ).grid(row=1, column=0)
        tk.Button(
            self,
            text="Settings",
            command=self._settingsButtonBind,
            font=("Arial", 20),
        ).grid(row=2, column=0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _key(self, event: Event) -> None:
        key: str = event.keysym
        match key:
            case "Escape":
                self.controller.destroy()
            case _:
                pass

    def bindKeyboard(self) -> None:
        """
        Bind the current screen keys
        """
        self.unbind_all("<Key>")
        self.bind_all("<Key>", self._key)

    def _newGameButtonBind(self) -> None:
        self.controller.reset()
        self.controller.showScreen("GameScreen")

    def _continueGameButtonBind(self) -> None:
        self.controller.showScreen("GameScreen")

    def _settingsButtonBind(self) -> None:
        raise NotImplementedError
