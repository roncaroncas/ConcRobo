import tkinter as tk
from tkinter import font  as tkfont

class StartView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		numColumns = 3
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)


		label = tk.Label(self, text="Concremat \n Zinho", font=gui.h1_font, borderwidth=2, relief="groove")
		label.grid(row=0, column=1, sticky="WENS", padx=5, pady=10, ipadx=5, ipady=10)

		buttonConnect = tk.Button(self, text="Conectar",
							font=gui.button_font,
							command=lambda: gui.show_frame("SetupConnectView"))

		buttonInstuct = tk.Button(self, text="Instruções",
							font=gui.button_font,
							command=lambda: gui.show_frame("HelpView"))



		buttonAdvanced = tk.Button(self, text="Avançado",
							font=gui.button_font,
							command=lambda: gui.show_frame("AdvancedView"))

		e = tk.Entry(self)

		buttonConnect.grid(column=1, sticky="WENS", padx=5, pady=5)
		buttonInstuct.grid(column=1, sticky="WENS", padx=5, pady=5)
		buttonAdvanced.grid(column=1, sticky="WENS", padx=5, pady=5)

		
	def ping(self):
		print("Hello!")

	def refreshFrame(self, state):
		pass