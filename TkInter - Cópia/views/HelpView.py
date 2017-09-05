import tkinter as tk
from tkinter import font  as tkfont

class HelpView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		numColumns = 3

		for i in range(numColumns):
			self.columnconfigure(i, weight=1)

		self.columnconfigure(1, minsize=300)

		self.draw()


	def draw(self):

		tk.Label(
			self, self.gui.border, text="Instruções", font=self.gui.h1_font
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

		
		# text = ("Para mover, use as teclas:\n"
		# 	"	Q W E\n" 
		# 	"	A S D\n" 
		# 	"	Z X C\n\n"

		# 	"Para voltar, aperte ESC\n\n" 

		# 	"Você deve monitorar o Zinho\n"
		# 	"e garantir condições seguras!\n\n"
						
		# 	"Você tem acesso a:\n"
		# 	" - Temperatura\n"
		# 	" - Pressao\n"
		# 	" - Inclinação\n"
		# 	" - Tensão da Bateria,\n"
		# 	" - Velocidade aproximada\n"
		# 	" - Distancia percorrida\n\n"

		# 	"Em relação a posição inicial,\n" 
		# 	"XYZ representam respectivamente:\n"
		# 	" - esquerda (-) ~ direita (+) \n"
		# 	" - trás     (-) ~ frente  (+) \n"
		# 	" - baixo    (-) ~ cima    (+)\n"
		# 	 )
