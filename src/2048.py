"""2048 Gmae"""  # pylint: disable=C0103

# for switching screens: https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

from Game import Game


def main() -> None:
    """Entry point of the game"""
    with Game() as g:
        # g.root.withdraw()
        g.mainloop()


if __name__ == "__main__":
    main()
