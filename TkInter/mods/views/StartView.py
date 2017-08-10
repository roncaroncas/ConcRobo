import tkinter as tk
from tkinter import font  as tkfont

class StartView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		numColumns = 3
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)


		label = tk.Label(self, text="Concremat \n Zinho", font=gui.h1_font)
		label.grid(row=0, column=1)

		buttonConnect = tk.Button(self, text="Conectar",
							font=gui.button_font,
							command=lambda: gui.show_frame("SetupConnectView"))

		buttonInstuct = tk.Button(self, text="Instruções",
							font=gui.button_font,
							command=lambda: gui.show_frame("HelpView"))



		buttonAdvanced = tk.Button(self, text="Avançado",
							font=gui.button_font,
							command=lambda: gui.show_frame("AdvancedView"))

		# newRoute = tk.IntVar()
		# buttonNewRoute = tk.Checkbutton(self, text="Escolha o ID", variable=newRoute)

		# buttonPing = tk.Button(self, text="Ping",
		# 					height=2, width=8,
		# 					command=self.ping)

		e = tk.Entry(self)

		buttonConnect.grid(column=1, sticky="NSEW")
		buttonInstuct.grid(column=1, sticky="NSEW")
		buttonAdvanced.grid(column=1, sticky="NSEW")
		# buttonNewRoute.grid(column=1, sticky="NSEW")
		# buttonPing.grid(column=1, sticky="NSEW")
		# e.grid(column=1, sticky="NSEW")

		
	def ping(self):
		print("Hello!")

	def refreshFrame(self, state):
		pass