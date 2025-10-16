"""The game itself"""

import tkinter as tk
from types import TracebackType
from src import Grid
from src.Screens import GameScreen, MainMenuScreen, MyScreen, SettingsScreen
from src.Utils import Screens


class Game(tk.Tk):
    """Game class where all the magic happens"""

    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.grid: Grid.Grid = Grid.Grid()
        self.title("2048")
        self.mainframe: tk.Frame = tk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S)
        self._current_frame: tk.Frame
        self._frames: dict[Screens, MyScreen] = {}
        for i, f in enumerate((GameScreen, MainMenuScreen, SettingsScreen)):
            frame = f(parent=self.mainframe, controller=self)
            self._frames[Screens(i)] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showScreen(Screens.MAIN_MENU)
        self.is_root_alive: bool = True

    def showScreen(self, screen: Screens) -> None:
        """Show a screen"""
        self._current_frame = self._frames[screen]
        if isinstance(self._current_frame, SettingsScreen):
            self._current_frame.setSettings()
        self._current_frame.bindKeyboard()
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
        self.quit()

    def reset(self) -> None:
        """Reset the game"""
        frame = self._frames[Screens.GAME]
        assert isinstance(frame, GameScreen)
        frame.reset()

    def getSettingsParameters(self) -> tuple[int, int, float, float]:
        """
        Get the settings parameters

        Returns:
            tuple[int, int, float, float]: win, base_color, start_tone, end_tone
        """
        return (
            self._frames[Screens.GAME].win,
            self._frames[Screens.GAME].base_color,
            self._frames[Screens.GAME].start_color,
            self._frames[Screens.GAME].end_color,
        )

    def setGameSettings(self, /, win: int, base: int, start: float, end: float) -> None:
        """To be used when the settings have been done"""
        self._frames[Screens.GAME].win = win
        self._frames[Screens.GAME].base_color = base
        self._frames[Screens.GAME].start_color = start
        self._frames[Screens.GAME].end_color = end
        game = self._frames[Screens.GAME]
        assert isinstance(game, GameScreen)
        game.generateColors()
