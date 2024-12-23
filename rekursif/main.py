import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

# Sample word list
word_list = ["PYTHON", "KIVY", "HANGMAN", "PROGRAMMING", "DEVELOPER"]

class HangmanApp(App):
    def build(self):
        self.word = self.get_word()
        self.word_completion = "_" * len(self.word)
        self.guessed_letters = []
        self.tries = 6

        self.layout = BoxLayout(orientation='vertical')
        self.hangman_label = Label(text=self.display_hangman(self.tries), font_size=20)
        self.word_label = Label(text=self.word_completion, font_size=24)
        self.input_box = TextInput(hint_text='Guess a letter or word', multiline=False)
        self.guess_button = Button(text='Guess', on_press=self.make_guess)

        self.layout.add_widget(self.hangman_label)
        self.layout.add_widget(self.word_label)
        self.layout.add_widget(self.input_box)
        self.layout.add_widget(self.guess_button)

        return self.layout

    def get_word(self):
        return random.choice(word_list).upper()

    def make_guess(self, instance):
        guess = self.input_box.text.upper()
        self.input_box.text = ''
        self.process_guess(guess)

    def process_guess(self, guess):
        if self.tries <= 0:
            self.show_popup("Sorry, you ran out of tries. The word was " + self.word + ". Maybe next time!")
            return

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                self.show_popup("You already guessed the letter " + guess)
            elif guess not in self.word:
                self.tries -= 1
                self.guessed_letters.append(guess)
                self.show_popup(guess + " is not in the word.")
            else:
                self.guessed_letters.append(guess)
                self.word_completion = ''.join(
                    [letter if letter in self.guessed_letters else '_' for letter in self.word]
                )
                if "_" not in self.word_completion:
                    self.show_popup("Congrats, you guessed the word! You win!")
                    return
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess != self.word:
                self.tries -= 1
                self.show_popup(guess + " is not the word.")
            else:
                self.word_completion = self.word
                self.show_popup("Congrats, you guessed the word! You win!")
                return
        else:
            self.show_popup("Not a valid guess.")

        self.hangman_label.text = self.display_hangman(self.tries)
        self.word_label.text = self.word_completion

        # Recursively prompt for the next guess
        if self.tries > 0 and "_" in self.word_completion:
            self.input_box.focus = True

    def display_hangman(self, tries):
        stages = [
            """
               --------
               |      |
               |      O
               |     \|/
               |      |
               -
            """,
            """
               --------
               |      |
               |      O
               |     \|/
               |      |
               |     / 
               -
            """,
            """
               --------
               |      |
               |      O
               |     \|/
               |      |
               |      
               -
            """,
            """
               --------
               |      |
               |      O
               |     \|
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |      |
               |      |     
               -
            """,
            """
               --------
               |      |
               |      O    
               |      
               |     
               -
            """,
            """
               --------
               |      |
               |          
               |      
               |     
               -
            """
        ]
        return stages[tries]

    def show_popup(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__":
    HangmanApp().run()
