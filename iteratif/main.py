import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class HangmanGame(BoxLayout):
    def __init__(self, **kwargs):
        super(HangmanGame, self).__init__(**kwargs)
        self.word_list = ['apple', 'banana', 'mango', 'strawberry', 'orange']
        self.start_game()

    def start_game(self):
        self.word = random.choice(self.word_list)
        self.word_completion = "_" * len(self.word)
        self.guessed_letters = []
        self.tries = 6

        self.clear_widgets()
        self.add_widget(Label(text="Let's play Hangman!"))
        self.hangman_label = Label(text=self.display_hangman(self.tries))
        self.add_widget(self.hangman_label)
        self.word_label = Label(text=self.word_completion)
        self.add_widget(self.word_label)

        self.guess_input = TextInput(hint_text='Guess a letter', multiline=False)
        self.add_widget(self.guess_input)

        self.guess_button = Button(text='Guess')
        self.guess_button.bind(on_press=self.make_guess)
        self.add_widget(self.guess_button)

    def make_guess(self, instance):
        guess = self.guess_input.text.lower()
        self.guess_input.text = ''

        if guess in self.guessed_letters:
            self.word_label.text = "You already guessed that letter."
        elif guess not in self.word:
            self.tries -= 1
            self.guessed_letters.append(guess)
            self.word_label.text = "Incorrect guess."
        else:
            self.guessed_letters.append(guess)
            self.word_completion = "".join([letter if letter in self.guessed_letters else "_" for letter in self.word])
            self.word_label.text = self.word_completion

        self.hangman_label.text = self.display_hangman(self.tries)

        if "_" not in self.word_completion:
            self.word_label.text = f"Congratulations! You've guessed the word: {self.word}"
            self.add_try_again_button()
        elif self.tries == 0:
            self.word_label.text = f"Sorry, you lost! The word was: {self.word}"
            self.add_try_again_button()

    def add_try_again_button(self):
        self.guess_button.disabled = True
        self.try_again_button = Button(text='Try Again')
        self.try_again_button.bind(on_press=self.start_game)
        self.add_widget(self.try_again_button)

    def display_hangman(self, tries):
        stages = [  # final state: head, body, both arms, and both legs
            """
               -----
               |   |
               |   O
               |  /|\\
               |  / \\
               -
            """,
            # head, body, one arm, one leg
            """
               -----
               |   |
               |   O
               |  /|\\
               |  /
               -
            """,
            # head, body, one arm
            """
               -----
               |   |
               |   O
               |  /|
               |
               -
            """,
            # head, body
            """
               -----
               |   |
               |   O
               |   |
               |
               -
            """,
            # head
            """
               -----
               |   |
               |   O
               |
               |
               -
            """,
            # initial empty state
            """
               -----
               |   |
               |
               |
               |
               -
            """
        ]
        return stages[min(max(0, tries), len(stages) - 1)]  # Ensure tries is within valid range

class HangmanApp(App):
    def build(self):
        return HangmanGame()

if __name__ == "__main__":
    HangmanApp().run()