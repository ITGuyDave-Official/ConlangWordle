import tkinter as tk
import random

# Load words from dictionary file
with open("dictionary.txt", "r") as file:
    words = [line.strip().upper() for line in file.readlines()]

# Choose a random word for the player to guess
solution_word = random.choice(words)

# Define the main application class
class WordleGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordle Clone")
        self.geometry("400x600")
        self.configure(bg="black")
        
        self.guess_number = 0
        self.max_guesses = 6
        self.word_length = 5

        # Create a frame to hold the guess boxes
        self.frames = [tk.Frame(self, bg="black") for _ in range(self.max_guesses)]
        for i, frame in enumerate(self.frames):
            frame.grid(row=i, column=0, pady=10)

        self.entry_boxes = [[tk.Label(frame, text="", font=("Helvetica", 24), width=2, height=1, borderwidth=2, relief="solid", bg="white") for _ in range(self.word_length)] for frame in self.frames]
        for i, row in enumerate(self.entry_boxes):
            for j, label in enumerate(row):
                label.grid(row=0, column=j, padx=5)

        self.current_guess = [""] * self.word_length

        # Create an entry box for letter input
        self.input_entry = tk.Entry(self, font=("Helvetica", 24), width=5)
        self.input_entry.grid(row=self.max_guesses, column=0, pady=20)
        self.input_entry.bind("<Return>", self.check_guess)
        self.input_entry.focus_set()

        # Display a message at the bottom
        self.message_label = tk.Label(self, text="", font=("Helvetica", 16), fg="white", bg="black")
        self.message_label.grid(row=self.max_guesses + 1, column=0)

    def check_guess(self, event):
        guess = self.input_entry.get().upper()
        if len(guess) != self.word_length or guess not in words:
            self.message_label.config(text="Invalid word. Try again!")
            return

        self.message_label.config(text="")
        self.update_display(guess)
        self.input_entry.delete(0, tk.END)
        self.guess_number += 1

        if guess == solution_word:
            self.message_label.config(text="Congratulations! You've guessed the word!")
            self.input_entry.config(state="disabled")
        elif self.guess_number == self.max_guesses:
            self.message_label.config(text=f"Game Over! The word was {solution_word}.")
            self.input_entry.config(state="disabled")

    def update_display(self, guess):
        correct_count = [0] * self.word_length
        solution_copy = list(solution_word)

        # First, mark all correct letters (green)
        for i, letter in enumerate(guess):
            if letter == solution_word[i]:
                label = self.entry_boxes[self.guess_number][i]
                label.config(text=letter, bg="green")
                correct_count[i] = 1
                solution_copy[i] = None  # Mark this letter as matched

        # Now mark letters that are correct but in the wrong position (yellow)
        for i, letter in enumerate(guess):
            if correct_count[i] == 0:  # If it's not already marked green
                if letter in solution_copy:
                    label = self.entry_boxes[self.guess_number][i]
                    label.config(text=letter, bg="yellow")
                    solution_copy[solution_copy.index(letter)] = None  # Mark this letter as used
                else:
                    label = self.entry_boxes[self.guess_number][i]
                    label.config(text=letter, bg="gray")



if __name__ == "__main__":
    app = WordleGame()
    app.mainloop()
