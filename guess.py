import sys
import random
import requests

VERSION = 1.0
URL = "https://random-word-api.herokuapp.com/word"
FALLBACK_WORDS = [
    "python", "programming", "developer", "terminal", "computer",
    "keyboard", "monitor", "router", "motherboard", "speaker",
]


def get_random_word(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raising error for HTTP errors

        return response.json()[0].lower()
    except (requests.RequestException, ValueError, IndexError, AttributeError):
        return random.choice(FALLBACK_WORDS)


def get_underscore_indices(character_list: list[str]) -> list[int]:
    return [
        i for i, ch in enumerate(character_list)
        if ch == '_' and 0 < i < (len(character_list) - 1)
    ]


def generate_hint(display_characters: list[str], secret_word: str) -> list[str]:
    if len(display_characters) < 2:
        return []

    underscore_indices = get_underscore_indices(display_characters)
    underscore_num = len(underscore_indices)

    if underscore_num < 3:
        return []

    sample_size = 5 if underscore_num >= 10 else 2
    hint_sample = random.sample(underscore_indices, k=sample_size)
    hint_list = [secret_word[i] for i in hint_sample]

    return [secret_word[0], secret_word[-1], *hint_list]


def get_user_input(display_string: str, interruption_string: str) -> str:
    try:
        return input(display_string).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{interruption_string}")
        sys.exit(0)


def get_display_word(guessed_letters: set[str], secret_word: str) -> list[str]:
    return [letter if letter in guessed_letters else '_' for letter in secret_word]


def play_game():
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"Welcome to CLI word guessing game v{VERSION}")
    print("Fetching Word...")

    secret_word = get_random_word(URL)

    guessed_letters: set[str] = set()
    wrong_words: set[str] = set()
    lives = 6
    hint_given = False

    while lives > 0:
        display_word = get_display_word(guessed_letters, secret_word)

        # Give the hint only once, when the player is down to their last 2 lives
        hint_message = None
        if lives == 2 and not hint_given:
            hint_given = True
            guessed_letters.update(generate_hint(display_word, secret_word))
            display_word = get_display_word(guessed_letters, secret_word)
            hint_message = (
                f"{BOLD}\n💡 Need a hint, Here's a letter map hint: "
                f"{''.join(display_word)}{RESET}"
            )

        if '_' not in display_word:
            print(f"\n🎉 Congratulations! You guessed the word: {secret_word.upper()}!")
            return

        print(f"\nWord: {''.join(display_word)}")
        print(f"Lives remaining: {lives}")

        if hint_message:
            print(hint_message)

        guess = get_user_input(
            "Guess a letter (or the whole word): ", "Game abandoned 🥲 Goodbye!"
        )

        if not guess.isalpha():
            print(f"{BOLD}⚠️ Please enter letters only.{RESET}")
            continue

        if len(guess) > 1:
            if guess == secret_word:
                print(f"\n🎉 Amazing guess! The word was indeed: {secret_word.upper()}!")
                return

            if guess in wrong_words:
                print(f"{BOLD}⚠️ You already tried '{guess}'. Try something else.{RESET}")
                continue

            wrong_words.add(guess)
            print(f"❌ '{guess}' is not the secret word!")
            lives -= 1
            continue

        if guess in guessed_letters:
            print(f"{BOLD}⚠️ You already guessed the letter '{guess}'. Try a different one.{RESET}")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"{BOLD}✅ Nice! '{guess}' is in the word.{RESET}")
        else:
            print(f"{BOLD}❌ Sorry, '{guess}' is not in the word.{RESET}")
            lives -= 1

    print(f"\n💥 Game Over! You ran out of lives. The word was: {secret_word.upper()}")


if __name__ == "__main__":
    while True:
        play_game()
        print('-' * 40)
        play_again = get_user_input("Play again? (Y/n) ", "Have a good day 😁")

        if play_again not in ("", "y", "yes"):
            print("Thanks for playing 😊")
            break