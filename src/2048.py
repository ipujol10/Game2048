"""2048 Gmae"""  # pylint: disable=C0103

from Game import Game


def main() -> None:
    """Entry point of the game"""
    with Game() as g:
        # g.root.withdraw()
        g.window.mainloop()


if __name__ == "__main__":
    main()
