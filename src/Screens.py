"""
File with the different screens of the game
"""

from itertools import repeat
import tkinter as tk
from tkinter import Event, messagebox, PhotoImage
from typing import Callable, TYPE_CHECKING, Any
from random import choice, random
from abc import ABC, abstractmethod
import math
import re
from src import Grid
from src.Utils import Color, Directions, Screens, Popouts

if TYPE_CHECKING:
    from Game import Game


class MyScreen(ABC, tk.Frame):
    """Interface for Screens"""

    def __init__(self, parent: tk.Frame, controller: "Game") -> None:
        tk.Frame.__init__(self, master=parent)
        self.controller: "Game" = controller
        self.win: int
        self.base_color: int
        self.start_color: float
        self.end_color: float

    def bindKeyboard(self) -> None:
        """
        Bind the current screen keys
        """
        self.unbind_all("<Key>")
        self.bind_all("<Key>", self._key)

    @abstractmethod
    def _key(self, event: Event) -> None:
        """Define how the program will react to the keyboard input"""


class GameScreen(MyScreen):
    """
    The screen with the game
    """

    def __init__(self, parent: tk.Frame, controller: "Game") -> None:
        MyScreen.__init__(self, parent, controller)

        self.matrix: Grid.Grid = Grid.Grid()
        self.gui_grid: list[list[tk.Label]]
        self._colors: dict[int, Color]

        self.bind_all("<Key>", self._key)
        self._directions: list[str] = [el.name for el in Directions]
        self._dir_func: dict[str, Callable[[], bool]] = {
            direction: function
            for direction, function in zip(
                self._directions, [self.matrix.up, self.matrix.left, self.matrix.down, self.matrix.right]
            )
        }

        self.win = 2048
        self.base_color = 165
        self.start_color = 100
        self.end_color = 66.4

        self.gui_grid = self._generateTiles()
        self.generateColors()

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

    def generateColors(self) -> None:
        """Generate the colors of the tiles"""
        hue = self.base_color
        start_lightness = self.start_color
        end_lightness = self.end_color
        keys: list[int] = [0, 2]
        while keys[-1] < self.win:
            keys.append(keys[-1] * 2)
        steps: int = len(keys) - 1
        delta: float = (end_lightness - start_lightness) / steps

        colors: dict[int, Color] = {}
        for i, key in enumerate(keys):
            lightness = start_lightness + delta * i
            colors[key] = Color(hue, 100, lightness)
        self._colors = colors

    def isEndgame(self) -> bool:
        """
        Checks if the player has won
        """
        if any(self.win in row for row in self.matrix.grid):
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
                self.gui_grid[i][j].config(
                    text=("" if value == 0 else str(value)), background=self._colors[value].rgb()
                )

    def _key(self, event: Event) -> None:
        key: str = event.keysym
        moved: bool = False
        match key:
            case "Escape":
                self.controller.showScreen(Screens.MAIN_MENU)
                return
            case val if val in self._directions:
                moved = self._dir_func[val]()
            case _:
                pass

        if self.isEndgame():
            self.reset()
            self.controller.showScreen(Screens.MAIN_MENU)
            return

        if moved:
            self.newTile()
        self.draw()

    def reset(self) -> None:
        """Reset the game"""
        self.matrix.reset()
        for _ in repeat(None, 2):
            self.newTile()
        self.matrix.updateAvailableSpace()
        self.draw()


class MainMenuScreen(MyScreen):
    """
    Main Menu screen class
    """

    def __init__(self, parent: tk.Frame, controller: "Game") -> None:
        MyScreen.__init__(self, parent, controller)

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

    def _newGameButtonBind(self) -> None:
        self.controller.reset()
        self.controller.showScreen(Screens.GAME)

    def _continueGameButtonBind(self) -> None:
        self.controller.showScreen(Screens.GAME)

    def _settingsButtonBind(self) -> None:
        self.controller.showScreen(Screens.SETTINGS)


class SettingsScreen(MyScreen):
    """Screen where you can tweek settings"""

    def __init__(self, parent: tk.Frame, controller: "Game") -> None:
        MyScreen.__init__(self, parent, controller)
        self._win: tk.Entry

        self._win = tk.Entry(self, width=20)
        self._win.grid(column=2, row=0)
        tk.Label(self, text="Win at:").grid(column=0, row=0, columnspan=2)

        self._color_image = PhotoImage(file="data/hue.png")
        tk.Label(self, image=self._color_image).grid(row=1, column=0, columnspan=3)

        tk.Label(self, text="Set base color (0-255)").grid(column=0, row=2)
        self._base_color: tk.Button = tk.Button(
            self,
            height=1,
            width=2,
            command=lambda: self._popout(Popouts.BASE),
        )
        self._base_color.grid(column=1, row=2)
        self._base_color_entry: tk.Entry = tk.Entry(self, width=5)
        self._base_color_entry.grid(column=2, row=2)

        tk.Label(self, text="Set start tone (0-100)").grid(column=0, row=3)
        self._start_color: tk.Button = tk.Button(self, height=1, width=2, command=lambda: self._popout(Popouts.START))
        self._start_color.grid(column=1, row=3)
        self._start_color_entry: tk.Entry = tk.Entry(self, width=10)
        self._start_color_entry.grid(column=2, row=3)

        tk.Label(self, text="Set end tone (0-100)").grid(column=0, row=4)
        self._end_color: tk.Button = tk.Button(self, height=1, width=2, command=lambda: self._popout(Popouts.END))
        self._end_color.grid(column=1, row=4)
        self._end_color_entry: tk.Entry = tk.Entry(self, width=10)
        self._end_color_entry.grid(column=2, row=4)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def _key(self, event: Event) -> None:
        key: str = event.keysym
        match key:
            case "Escape":
                self.saveSettings()
                self.controller.showScreen(Screens.MAIN_MENU)
            case "Return":
                self.saveSettings()
                self.setSettings()
            case _:
                pass

    def setSettings(self) -> None:
        """Set the settings screen with the current values"""
        win, base, start, end = self.controller.getSettingsParameters()
        self._win.delete(0, tk.END)
        self._win.insert(0, str(win))

        self._base_color_entry.delete(0, tk.END)
        self._base_color_entry.insert(0, str(base))
        self._base_color.config(background=Color(base, 100, 50).rgb())

        self._start_color_entry.delete(0, tk.END)
        self._start_color_entry.insert(0, str(start))
        self._start_color.config(background=Color(base, 100, start).rgb())

        self._end_color_entry.delete(0, tk.END)
        self._end_color_entry.insert(0, str(end))
        self._end_color.config(background=Color(base, 100, end).rgb())

    def saveSettings(self) -> None:
        """Save the settings into game"""
        win: int = self._correctWinInputPower(self._win.get())
        base: int = int(self._correctInput(self._base_color_entry.get(), 255))
        base = int(self._base_color_entry.get()) if base == -1 else base
        start: float = self._correctInput(self._start_color_entry.get())
        start = float(self._start_color_entry.get()) if start == -1 else start
        end: float = self._correctInput(self._end_color_entry.get())
        end = float(self._end_color_entry.get()) if end == -1 else end
        self.controller.setGameSettings(win, base, start, end)

    def _correctWinInputPower(self, user_input: str) -> int:
        regex: str = r"^\d+(\.\d+)?$"
        if not bool(re.match(regex, user_input)):
            self._dialogBox("Input error", "Not a number")
            return self.controller.getSettingsParameters()[0]
        number: int = int(float(user_input))
        log: int = int(math.log2(number))
        return 2**log

    def _correctInput(self, user_input: str, limit: int = 100) -> float:
        regex: str = r"^\d+(\.\d+)?$"
        if not bool(re.match(regex, user_input)):
            self._dialogBox("Input error", "Not a number")
            return -1
        return min(max(float(user_input), 0), limit)

    def _dialogBox(self, title: str, message: str) -> None:
        messagebox.showwarning(title=title, message=message)

    def _popout(self, pop_type: Popouts) -> Any:
        SelectColor.getInstance(self.controller, pop_type.name.capitalize())


class SelectColor(tk.Toplevel):
    """Create a new window to select the colors with the mouse"""

    _instance = None

    def __init__(self, master: "Game", title: str) -> None:
        if SelectColor._instance is not None:
            raise ValueError("Already exists!")
        tk.Toplevel.__init__(self, master=master)
        self._setupWindow(title)

    def _setupWindow(self, title: str) -> None:
        self.title(title)
        self.geometry("550x150")

        self.protocol("WM_DELETE_WINDOW", self._onClose)

    def _onClose(self):
        SelectColor._instance = None
        self.destroy()

    @staticmethod
    def getInstance(master: "Game", title: str) -> "SelectColor":
        """Get the window instance if it exists or create one if not"""
        if SelectColor._instance is None:
            SelectColor._instance = SelectColor(master, title)
        return SelectColor._instance
