import sys
import random
import requests

VERSION = 1.0
URL = "https://random-word-api.herokuapp.com/word"

def get_random_word(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Rasing error for HTTP errors

        return response.json()[0]
    except Exception:
         fallback_words = ["python", "programming", "developer", "terminal", "computer", "keyboard", "monitor", "router", "motherboard", "speaker"]
         return random.choice(fallback_words)

def get_underscore_indices(guess_word: str) -> list[int]:
    return [i for i, chr in enumerate(guess_word) if chr == '_']

def generate_hint(guess_word: str, secret_word: str) -> str:
    hint_word = list(guess_word)
    word_length = len(hint_word)
    if word_length < 2:
        return guess_word

    underscore_indices = get_underscore_indices(guess_word)

    underscore_num = len(underscore_indices)

    if underscore_num < 3:
        return guess_word

    sample_size = 5 if underscore_num > 10 else (3 if underscore_num > 5 else 2)

    hint_sample = random.sample(underscore_indices, k=sample_size)

    for hint in hint_sample:
        hint_word[hint] = secret_word[hint]

    return "".join(hint_word)



def play_game():

    print("Welcome to CLI word guessing game")
    print("Fetching Word...")

    secret_word = get_random_word(URL)
    word_length = len(secret_word)

    guessed_letter = set()
    lives = 6

    display_word = []

    while lives > 0:
        for letter in secret_word:
            if letter in guessed_letter:
                display_word.append(letter)
            else:
                display_word.append('_')

        if '_' not in display_word:
            print(f"\n🎉 Congratulations! You guessed the word: {secret_word.upper()}!")
            return

        current_word = "".join(display_word)
        print(f"\nWord: {current_word}")
        print(f"lives remaining: {lives}")

        guess = input("Guess a letter(or full word): ").strip().lower()

        if guess == secret_word:
            print("")

if __name__ == "__main__":
    pass

"""
import sys
import random
import requests

def fetch_secret_word():

    url = "https://herokuapp.com"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        # API returns a list, e.g., ["apple"]
        return response.json()[0].lower()
    except Exception:
        # Fallback list if the API is offline or there's no internet connection
        fallback_words = ["python", "programming", "developer", "terminal", "computer", "keyboard"]
        return random.choice(fallback_words)

def generate_hint(word):

    if len(word) <= 2:
        return word
    return f"{word[0]}{'_' * (len(word) - 2)}{word[-1]}"

def play_game():
    print("Welcome to the CLI Word Guessing Game!")
    print("Fetching a secret word from the API...")
    
    secret_word = fetch_secret_word()
    word_length = len(secret_word)
    
    # Track letters guessed correctly by the user
    guessed_letters = set()
    lives = 6
    
    print("\nWord found! Let's begin.")
    
    while lives > 0:
        # 1. Display current progress (e.g., p _ _ t h _ n)
        display_word = []
        for letter in secret_word:
            if letter in guessed_letters:
                display_word.append(letter)
            else:
                display_word.append("_")
        
        current_progress = " ".join(display_word)
        print(f"\nWord: {current_progress}")
        print(f"Lives remaining: {lives}")
        
        # Check if the player has uncovered all letters
        if "_" not in display_word:
            print(f"\n🎉 Congratulations! You guessed the word: {secret_word.upper()}!")
            return

        # 2. Offer a hint automatically if they are struggling
        if lives <= 2:
            print(f"💡 Need a hand? Here's a letter map hint: {generate_hint(secret_word)}")

        # 3. Get user input
        try:
            guess = input("Guess a letter (or the whole word): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nGame abandoned. Goodbye!")
            sys.exit()

        if not guess:
            print("Please type something!")
            continue

        # 4. Handle whole-word guess
        if len(guess) > 1:
            if guess == secret_word:
                print(f"\n🎉 Amazing guess! The word was indeed: {secret_word.upper()}!")
                return
            else:
                print(f"❌ '{guess}' is not the secret word!")
                lives -= 1
                continue

        # 5. Handle single-letter guess
        if guess in guessed_letters:
            print(f"⚠️ You already guessed the letter '{guess}'. Try a different one.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"✅ Nice! '{guess}' is in the word.")
        else:
            print(f"❌ Sorry, '{guess}' is not in the word.")
            lives -= 1

    # Out of lives
    print(f"\n💥 Game Over! You ran out of lives. The word was: {secret_word.upper()}")

if __name__ == "__main__":
    while True:
        play_game()
        print("-" * 40)
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

"""