import random
import time

# Sample word list
word_list = ["PYTHON", "KIVY", "HANGMAN", "PROGRAMMING", "DEVELOPER", "UNCOPYRIGHTABLE", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

class Hangman:
    def __init__(self, word=None):
        self.word = word if word else random.choice(word_list).upper()
        self.word_completion = "_" * len(self.word)
        self.guessed_letters = []
        self.tries = 6

    def make_guess(self, guess):
        guess = guess.upper()

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                return "Already guessed"
            elif guess not in self.word:
                self.tries -= 1
                self.guessed_letters.append(guess)
                return f"{guess} is not in the word."
            else:
                self.guessed_letters.append(guess)
                self.word_completion = ''.join(
                    [letter if letter in self.guessed_letters else '_' for letter in self.word]
                )
                if "_" not in self.word_completion:
                    return "You win!"
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess != self.word:
                self.tries -= 1
                return f"{guess} is not the word."
            else:
                self.word_completion = self.word
                return "You win!"
        else:
            return "Invalid guess."

        if self.tries <= 0:
            return f"Game over. The word was {self.word}."
        return "Keep going."

    def simulate_game(self, guesses):
        for guess in guesses:
            result = self.make_guess(guess)
            if "win" in result or "Game over" in result:
                break
        return result

# Test cases
def test_case(word, guesses):
    hangman = Hangman(word)
    start_time = time.perf_counter()  # Use perf_counter for better precision
    result = hangman.simulate_game(guesses)
    end_time = time.perf_counter()
    return result, end_time - start_time

# Define test cases
test_cases = [
    ("KIVY", ["K", "I", "V", "Y"]),  # Case 1: 4 inputs, all correct
    ("DEVELOPER", ["D", "E", "V", "L", "O", "P", "R"]),  # Case 2: 7 inputs, all correct
    ("UNCOPYRIGHTABLE", ["U", "N", "C", "O", "P", "Y", "R", "I", "G", "H", "T", "A", "B", "L", "E"]),  # Case 3
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),  # Case 4
]

# Run test cases
for i, (word, guesses) in enumerate(test_cases, 1):
    result, exec_time = test_case(word, guesses)
    print(f"Case {i}: Result = {result}, Execution Time = {exec_time:.6f} seconds")
