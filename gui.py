import tkinter as tk
from random import randint


class App:
	def __init__(self):
		self.root = tk.Tk()
		
		self.word, self.state = choose_word()

		self.turns = tk.IntVar(value=len(self.word)+3)

		self.set_window()
		self.set_menu()
		self.add_widgets()
		self.update_current_state()

		self.display()

	def set_window(self):
		self.root.title("Hangman game")
		#self.root.geometry(f"558x310")
		self.root.resizable(False, False)

	def set_menu(self):
		menu_bar = tk.Menu()

		jeu_menu = tk.Menu(menu_bar, tearoff=0)
		jeu_menu.add_command(label="Restart", command=self.restart)

		menu_bar.add_cascade(label="Game", menu=jeu_menu)

		self.root.config(menu=menu_bar)

	def add_widgets(self):
		letters="azertyuiopqsdfghjklmwxcvbn-".upper()

		scorebar = tk.Frame(self.root, height=40)
		scorebar.pack(fill="x")

		score_label = tk.Label(scorebar, text="Turns: ", font="Helvetica 16 bold")
		score_label.pack(side="right")
		score = tk.Label(scorebar, textvariable=self.turns, font="Helvetica 16 bold")
		score.pack(side="right", before=score_label, padx=(0, 20))
		
		output = tk.Frame(height=150)
		output.pack_propagate(False)
		output.pack(fill="both", expand=True)

		self.container = tk.Frame(output)
		self.container.pack(expand=True)

		self.buttons = tk.Frame(height=200)
		self.buttons.pack(fill="x", side="bottom")

		count=0
		for i in range(3):
			for j in range(9):
				btn = tk.Button(self.buttons, text=letters[count], font="Helvetica 16 bold", highlightthickness=1, width=4)

				if letters[count].lower() in self.state: btn.config(bg="#00ee00", activebackground="#00ee00")
				else: btn.bind("<Button-1>", lambda event, button=btn:self.play(button))

				btn.grid(row=i, column=j)
				count+=1

	def update_current_state(self):
		for widget in self.container.winfo_children():
			widget.destroy()

		for letter in self.state:
			label = tk.Label(self.container, bg='#fff', text=letter, font="Arial 20 bold")
			if letter!="_": label.config(bg="#00ee00")
			label.pack(side="left", expand=True, ipadx=10, ipady=10, padx=2)


	def play(self, button):
		l = button.cget("text").lower()

		if l in self.word and l not in self.state:
			for i in range(len(self.word)):
				if self.word[i] == l:
					self.state = self.state[:i] + l + self.state[i+1:]

			self.update_current_state()

			button.config(bg="#00ee00", activebackground="#00ee00")
		else:
			button.config(bg="#ee0000", activebackground="#ee0000")

		button.unbind("<Button-1>")
				
		self.turns.set(self.turns.get()-1)

		if self.word == self.state or self.turns.get()<=0:
			for child in self.root.winfo_children()[3].winfo_children():
				child.unbind("<Button-1>")
				child.config(bg="#808080", activebackground="#808080")

			self.root.winfo_children()[1].destroy()

			self.root.winfo_children()[1].winfo_children()[0].destroy()
			self.root.winfo_children()[1].config(bg="#808080")

			result = tk.Frame(self.root.winfo_children()[1], bg="#fff", height=150, width=400)
			result.pack_propagate(False)
			result.pack(pady=(30, 0))

			result_label = tk.Label(result, font="Calibri 18 bold", bg="#fff")
			result_text = tk.Label(result, font="Helvetica 12", bg="#fff")

			if self.word==self.state:
				result_label.config(text="Congratulations !!!", fg="#00ee00")

				result_text.config(text=f"You found the word: \"{self.word}\"")
			else:
				result_label.config(text="Game Over !!!", fg="#ee0000")

				result_text.config(text=f"You lose. The word was: \"{self.word}\"")

			result_label.pack(pady=(5, 0))
			result_text.pack(anchor="w", padx=(10, 0), pady=(12, 0))

			buttons = tk.Frame(result, bg="#fff")
			buttons.pack(side="bottom", fill="x", pady=(0, 10))

			restart = tk.Button(buttons, text="Restart", font="Helvetica 11 bold", width=8, command=lambda:self.root.after(100, self.restart))
			restart.pack(side="left", padx=(80, 0))

			quit = tk.Button(buttons, text="Quit ❌", width=8, font="Helvetica 11 bold", command=lambda:self.root.after(100, lambda:self.root.destroy()))
			quit.config(bg="#ee0000", activebackground="#ee0000")
			quit.pack(side="right", padx=(0, 80))

	def restart(self):
		self.root.destroy()
		App()

	def display(self):
		self.root.mainloop()

def choose_word():
	words = words = ["chat", "dog", "house", "car", "tree", "sun", "beach",
         "mountain", "book", "school", "computer", "music", "movie",
         "sport", "football", "basketball", "tennis", "cooking", "travel",
         "love", "family", "happiness", "health", "money", "time", "garden",
         "television", "radio", "internet", "phone", "photo", "nature", "city",
         "food", "drink", "party", "birthday", "christmas", "holiday",
         "spring", "summer", "autumn", "winter", "morning", "afternoon",
         "evening", "night", "laughter", "tears", "sleep"]

	word =  words[randint(0, len(words)-1)]
	letter = word[randint(0, len(word)-1)]
	current=""

	for i in range(len(word)):
		if word[i] == letter:
			current+=letter
		else:
			current +="_"

	return word,current

if __name__ == "__main__":
	App()