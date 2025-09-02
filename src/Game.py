"""The game itself"""

import tkinter as tk
from types import TracebackType
from tkinter import Event
from typing import Callable
import Grid
from Utils import Directions
from Screens import GameScreen


class Game(tk.Tk):
    """Game class where all the magic happens"""

    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.grid: Grid.Grid = Grid.Grid()
        self.title("2048")
        self.mainframe: tk.Frame = tk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S)
        self._current_frame: tk.Frame
        self._frames: dict[str, tk.Frame] = {}
        for F in (GameScreen,):
            screen_name: str = F.__name__
            frame = F(parent=self.mainframe, controller=self)
            self._frames[screen_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")  # pylint: disable=E1102
            self._current_frame = frame

        self.is_root_alive: bool = True
        self.bind_all("<Key>", self._key)
        self._directions: list[str] = [el.name for el in Directions]
        self._dir_func: dict[str, Callable[[], bool]] = {
            direction: function
            for direction, function in zip(
                self._directions, [self.grid.up, self.grid.left, self.grid.down, self.grid.right]
            )
        }

    def __enter__(self) -> "Game":
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.is_root_alive:
            self.destroy()

    def _destroy(self) -> None:
        self.is_root_alive = False
        self.destroy()

    def _key(self, event: Event) -> None:
        if isinstance(self._current_frame, GameScreen):
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

            if self._current_frame.isEndgame():
                self._destroy()

            if moved:
                self._current_frame.newTile()
            self._current_frame.draw()
