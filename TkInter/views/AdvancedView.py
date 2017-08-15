import tkinter as tk
from tkinter import font  as tkfont

class AdvancedView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		numColumns = 3
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)

		self.draw()

	def draw(self):

		tk.Label(
			self, self.gui.border, text="Configurações\nAvançadas", font=self.gui.h1_font
			).grid(
			self.gui.h1_pad, column=1, sticky="WENS")

		tk.Label(
			self, self.gui.border, text="EM BREVE", font=self.gui.h2_font
			).grid(
			self.gui.h2_pad, column=1, sticky="WENS")

		tk.Button(
			self, text="Voltar", command=lambda: self.gui.show_frame("Start")
			).grid(
			self.gui.button_pad, column=1, sticky="WENS")
