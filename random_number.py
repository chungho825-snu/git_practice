"""Print a random number between 1 and 100."""

from random import randint


def main() -> None:
    print(f"Today's random number: {randint(1, 100)}")


if __name__ == "__main__":
    main()
