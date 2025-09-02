"""The game itself"""

import tkinter as tk
from types import TracebackType
import Grid
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

            frame.grid(row=0, column=0, sticky="nsew")
            self._current_frame = frame

        self.is_root_alive: bool = True

        self._current_frame.tkraise()  # type: ignore

    def __enter__(self) -> "Game":
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.is_root_alive:
            self.destroy()

    def destroy(self) -> None:
        self.mainframe.tkraise()  # type:ignore
        self.is_root_alive = False
        self.destroy()
