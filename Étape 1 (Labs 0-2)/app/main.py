"""Main script that prints messages de motivations."""

import random


def get_random_message():
    """Return a random motivational message."""
    message = [
        "Keep it up :)",
        "You got this :)",
        "You're almost at the finish line :)",
        "It will be okay :)"
    ]
    return random.choice(message)


def main():
    """Print greeting and a random motivational message."""
    print("Hey you!")
    print(get_random_message())


if __name__ == "__main__":
    main()
    