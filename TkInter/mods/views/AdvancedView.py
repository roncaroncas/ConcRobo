import tkinter as tk
from tkinter import font  as tkfont

class AdvancedView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		numColumns = 3
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)


		label = tk.Label(self, text="Advanced", font=gui.h1_font)
		label.grid(column=1)

		self.text1 = tk.StringVar()
		self.text1.set("Apagar todos os percursos")

		button1 = tk.Button(self, textvariable=self.text1,
						   command=self.addOne)
		button1.grid(column=1)


		button2 = tk.Button(self, text="Voltar",
						   command=lambda: gui.show_frame("StartView"))
		button2.grid(column=1)

	def refreshFrame(self, state):
		if (state.n%2 == 1):
			self.text1.set("oi")
		else:
			self.text1.set("tchau")


	def addOne(self):
		self.controller.addOne()
