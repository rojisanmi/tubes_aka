import time

class Hangman:
    def __init__(self, word):
        self.word = word.upper()
        self.word_completion = "_" * len(self.word)
        self.guessed_letters = []
        self.tries = 6

    def process_guess(self, guess):
        if self.tries == 0:
            return f"Game over. The word was {self.word}."
        else:
            if len(guess) == 1 and guess.isalpha():
                if guess in self.guessed_letters:
                    self.tries -= 1
                    pass  # Already guessed
                elif guess not in self.word:
                    self.tries -= 1
                    self.guessed_letters.append(guess)
                else:
                    self.guessed_letters.append(guess)
                    self.word_completion = ''.join(
                        [letter if letter in self.guessed_letters else '_' for letter in self.word]
                    )
                    if "_" not in self.word_completion:
                        return "Congrats, you guessed the word!"
            elif len(guess) == len(self.word) and guess.isalpha():
                if guess != self.word:
                    self.tries -= 1
                else:
                    self.word_completion = self.word
                    return "Congrats, you guessed the word!"
            else:
                pass  # Invalid guess

            if self.tries == 0:
                return f"Game over. The word was {self.word}."
            elif "_" in self.word_completion:
                return None  # Continue game

# Test case execution with timing
def test_case(word, guesses):
    game = Hangman(word)
    start_time = time.perf_counter()  # Start timing
    result = None
    for guess in guesses:
        result = game.process_guess(guess)
        if result:
            break
    end_time = time.perf_counter()  # End timing
    return result, end_time - start_time

# Define test cases
test_cases = [
    ("KIVY", ["K", "I", "V", "Y"]),  # Case 1: Correct guesses
    ("DEVELOPER", ["D", "E", "V", "L", "O", "P", "R"]),  # Case 2: Correct guesses
    ("UNCOPYRIGHTABLE", ["U", "N", "C", "O", "P", "Y", "R", "I", "G", "H", "T", "A", "B", "L", "E"]),  # Case 3
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),  # Case 4
]

# Run test cases
for i, (word, guesses) in enumerate(test_cases, 1):
    result, exec_time = test_case(word, guesses)
    print(f"Case {i}: Result = {result}, Execution Time = {exec_time:.6f} seconds")
