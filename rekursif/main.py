import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from words import word_list


class HangmanApp(App):
    def build(self):
        # Inisialisasi data permainan
        self.word = self.get_word()
        self.word_completion = ["_"] * len(self.word)
        self.guessed_letters = []
        self.tries = 6

        # Membuat layout antarmuka
        layout = BoxLayout(orientation='vertical')
        self.word_label = Label(text=" ".join(self.word_completion))
        self.hangman_label = Label(text=self.display_hangman(self.tries))
        self.input_box = TextInput(hint_text='Guess a letter', multiline=False, input_filter='string')
        self.guess_button = Button(text='Guess')
        self.guess_button.bind(on_press=self.start_recursive_game)

        layout.add_widget(self.hangman_label)
        layout.add_widget(self.word_label)
        layout.add_widget(self.input_box)
        layout.add_widget(self.guess_button)

        return layout

    def get_word(self):
        # Mengambil kata acak dari word_list
        return random.choice(word_list).upper()

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

    def show_popup(self, message):
        popup = Popup(title='Notification',
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()

    def start_recursive_game(self, instance):
        # Memulai proses rekursif permainan
        self.guess_recursive()

    def guess_recursive(self):
        # Kondisi akhir (base case): menang atau kalah
        if "_" not in self.word_completion:
            self.show_popup(f"Congratulations! You guessed the word: {''.join(self.word_completion)}")
            return
        if self.tries == 0:
            self.show_popup(f"Game over! The word was: {self.word}")
            return

        # Proses input dan validasi
        guess = self.input_box.text.upper()
        self.input_box.text = ''  # Kosongkan kotak input
        if guess in self.guessed_letters:
            self.show_popup("You already guessed that letter.")
        elif len(guess) == 1 and guess.isalpha():
            self.guessed_letters.append(guess)
            if guess in self.word:
                for i, letter in enumerate(self.word):
                    if letter == guess:
                        self.word_completion[i] = guess
            else:
                self.tries -= 1
        else:
            self.show_popup("Invalid input. Please guess a single letter.")

        # Update tampilan
        self.word_label.text = " ".join(self.word_completion)
        self.hangman_label.text = self.display_hangman(self.tries)

        # Panggilan rekursif untuk langkah berikutnya
        self.guess_recursive()


# Menjalankan aplikasi
if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	HangmanApp().run()