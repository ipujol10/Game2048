"""Module to have utilities"""

from enum import Enum


class Directions(Enum):
    """Possible movements that the player can do in the game"""

    Up = 0  # pylint: disable=C0103
    Left = 1  # pylint: disable=C0103
    Down = 2  # pylint: disable=C0103
    Right = 3  # pylint: disable=C0103


class Screens(Enum):
    """An Enum with the different screens"""

    GAME = 0
    MAIN_MENU = 1
    SETTINGS = 2


class Popouts(Enum):
    """Type of popouts"""

    BASE = 0
    START = 1
    END = 2


class Color:
    """Color class to be able to work with HSl and RGB"""

    def __init__(self, hue: int, saturation: float, lightness: float) -> None:
        self.hue: int = hue
        self.saturation: float = saturation
        self.lighness: float = lightness

    def rgb(self) -> str:
        """
        Return the RGB value with the format "x{r:02x}{g:02x}{b:02x}"
        """
        return self._hsl2rgb(self.hue, self.saturation, self.lighness)

    def hsl(self) -> tuple[int, float, float]:
        """
        Return the HSL value with the format (H, S, L)
        H (int): [0,255]
        S (float): [0, 100]
        L (float): [0, 100]
        """
        return (self.hue, self.saturation, self.lighness)

    def _hsl2rgb(self, hue: int, saturation: float, lightness: float) -> str:
        """
        Function to convert a HSL value into an RGB

        Args:
            hue (int): The hue value in the range of [0, 255]
            saturation (float): The saturation value in the range of [0, 100]
            lightness (float): The lighness value in the range of [0, 100]

        Returns:
            str: The RGB value with the format "x{r:02x}{g:02x}{b:02x}"
        """
        h_norm: float = (hue % 256) / 256
        s_norm: float = saturation / 100
        l_norm: float = lightness / 100

        r: float
        g: float
        b: float
        if s_norm == 0:
            r = g = b = l_norm
        else:

            def hue2rgb(p: float, q: float, t: float) -> float:
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p

            q: float = l_norm * (1 + s_norm) if l_norm < 0.5 else l_norm + s_norm - l_norm * s_norm
            p: float = 2 * l_norm - q

            r = hue2rgb(p, q, h_norm + 1 / 3)
            g = hue2rgb(p, q, h_norm)
            b = hue2rgb(p, q, h_norm - 1 / 3)

        r = max(0, min(round(r * 256), 255))
        g = max(0, min(round(g * 256), 255))
        b = max(0, min(round(b * 256), 255))
        return f"#{r:02x}{g:02x}{b:02x}"
