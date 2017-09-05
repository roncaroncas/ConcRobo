'''
Cada View é um objeto do tipo tk.Frame

Possui 3 ponteiros:
- gui, para o pai de todos os gráficos
- controller, para ao objeto equivalente que possui os controles desse view
- parent, para o pai direto desse objeto 

Se necessário, importam-se as imagens

Declara-se todas as variáveis necessárias com objetivo de organizar o código.
Vale notar padrões estabelecidos na nomeação:
Str ou Int: 	var_NOME
Label:			valLb_NOME
Entry:			varEn_NOME
Image:			varIm_NOME

Faz-se o desenho de toda a página com a função draw()
	Primeiro, define-se o tamanho das colunas do frame através da função columnconfigure(column, regra)
	A função draw chama widgets do tipo Label, Entry, Button, Frame... e desenham em uma linha e uma coluna,
	Vale notar que quando-se chama um Frame, deve-se setar as colunas e criar seus próprios widgets Label, Entry, Button, Frame...
	Os parâmetros para cada tipo de widget variam e podem ser explorador melhor no site: http://effbot.org/tkinterbook/
	Apenas os widgets que precisam ser chamados pelo controller ficam guardados em uma variável

A função binder() relaciona os inputs do usuário (mouse/teclado) de todos os widgets a função equivalente em controller

'''

import tkinter as tk
from tkinter import font  as tkfont

class InstrucoesView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		#Setando as colunas
		self.columnconfigure(0, minsize=25)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, minsize=25)

		self.draw()

		
		#Seta os inputs
		self.binder()


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
			self, text="Voltar", command=lambda: self.gui.show_frame("Menu")
			).grid(
			self.gui.button_pad, column=1, sticky="WENS")

	def binder(self):

		self.bind("<Key>", self.controller.key)
		self.bind("<KeyRelease>", self.controller.keyRelease)
		self.bind("<Button-1>", self.controller.mouse)

		for wid in self.winfo_children():
			wid.bind("<Key>", self.controller.key)
			wid.bind("<KeyRelease>", self.controller.keyRelease)
			wid.bind("<Button-1>", self.controller.mouse)
		
			for wid2 in wid.winfo_children():
				wid2.bind("<Key>", self.controller.key)
				wid2.bind("<KeyRelease>", self.controller.keyRelease)
				wid2.bind("<Button-1>", self.controller.mouse)

		
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
