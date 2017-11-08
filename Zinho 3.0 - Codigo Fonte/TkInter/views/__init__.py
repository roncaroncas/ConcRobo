'''
A interface gráfica é feita a partir de Python + tkInter
Para ajudas com tkInter, vale a pena verificar o link: http://effbot.org/tkinterbook/

Essa estratégia funciona hierarquicamente, gera-se um objeto gráfico principal, e objetos filhos que podem ter mais filhos
Os filhos, são chamados Widgets, e são posicionados na tela através de uma função grid, que o posiciona em relação a uma linha
e uma coluna. Assim, se organiza a posição dos elementos da página através de uma "tabela invisível"

Por exemplo: Gera-se a janela principal, e dentro dela, gera-se frames, e dentro dos frames geram-se textos, etc...

Esse programa funciona da seguinte maneira:
Gera-se um objeto GUI com um ponteiro ao Client

Geram-se várias paginas (denomidas de frames), e são desenhadas sobrepostas uma a outra.
Apenas uma dessa páginas fica visível quando se coloca esse frame a frente dos demais, isso se faz através da função show_frame()

Cada uma dessas páginas deve estar em um arquivo separado onde cada uma delas possui um objeto com o nome "Frame+View", o nome da pagina
deve ser adicionado a variável chamada "paginas".
Cada View, deve ter seu arquivo equivalente em controller

Exemplo: A pagina menu deve estar organizada num arquivo "Menu.py" dentro da pasta "views" e deve possuir um objeto chamado "MenuView".
Além disso, deve haver um arquivo Menu.py na pasta controller com um objeto MenuController.

Esse arquivo chama todos os views guardando no dicionário ".frames", define alguns parâmetros de formatação por praticidade

'''
#IMPORT ALL
from .Menu import MenuView
from .Configuracoes import ConfiguracoesView
from .Instrucoes import InstrucoesView
from .Conectado import ConectadoView
from .Conectar import ConectarView
from .Creditos import CreditosView


import tkinter as tk
from tkinter import font  as tkfont
from tkinter import messagebox

class GUI(tk.Tk):

	def __init__(self, client):
		tk.Tk.__init__(self)

		###############################################################################################

		#Colocar o nome de Todas as páginas a serem criadas!
		#Cada página com o nome "name" deve ter um arquivo chamado "nameView" dentro da pasta "views" e
		#um arquivo "nameController" nas pasta "controler"
		paginas = ("Menu", "Conectar", "Conectado", "Instrucoes", "Configuracoes", "Creditos")

		###############################################################################################

		#Ponteiros
		self.client = client #Parent

		#Fonts
		self.h1_font = 		tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		self.h2_font = 		tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")
		self.p_font = 		tkfont.Font(family='Helvetica', size=10)
		self.button_font = 	tkfont.Font(family='Helvetica', size=10, weight="bold")

		#Pads
		self.h1_pad = 		{'padx':5, 'pady':10, 	'ipadx':5, 'ipady':10}
		self.h1_pad_compact={'padx':0, 'pady':10, 	'ipadx':5, 'ipady':10}
		self.h2_pad = 		{'padx':5, 'pady':5, 	'ipadx':2, 'ipady':2}
		self.h2_pad_compact={'padx':0, 'pady':5, 	'ipadx':2, 'ipady':2}
		self.p_pad = 		{'padx':5, 'pady':3, 	'ipadx':2, 'ipady':2}
		self.p_pad_compact ={'padx':0, 'pady':0, 	'ipadx':0, 'ipady':0}
		self.button_pad = 	{'padx':5, 'pady':5, 	'ipadx':2, 'ipady':2}
		self.button_pad_compact = {'padx':0, 'pady':5, 	'ipadx':2, 'ipady':2}

		#Border
		self.border = {"borderwidth":2, "relief":"groove"}

		#Define o que fazer caso o usuário aperte o X de fechar a janela
		self.protocol("WM_DELETE_WINDOW", self.client.on_exit)

		#Criando todas as Páginas
		container = tk.Frame()
		container.grid(sticky="nsew")
		self.frames = {}
		for F in paginas:
			page_name = F
			view = eval(page_name+"View")
			controller = eval("self.client.controller.controls['"+F+"']")
			frame = view(parent=container, controller=controller, gui=self)
			self.frames[page_name] = frame
			frame.grid(row=0, sticky="nsew")

			frame.bind("<Key>", self.key)
			frame.bind("<KeyRelease>", self.keyRelease)
			frame.bind("<Button-1>", self.mouse)

		#Fixa o tamanho da janela
		self.resizable(width=False, height=False)
		
		#Trás para frente a janela inicial Menu
		self.nowFrame = "Menu"
		frame = self.frames["Menu"]
		frame.focus_set()
		frame.tkraise()
		

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		self.frames[page_name].controller.show_frame()
		self.nowFrame = page_name

		#print(page_name)

		# self.nowFrame = page_name 
		# frame = self.frames[page_name]
		# frame.focus_set()
		# frame.tkraise()
		#print(self.frames[page_name].winfo_width(), self.frames[page_name].winfo_height())

	def refreshAll(self, models):
		self.frames[self.nowFrame].controller.refresh(models)
		
	def key(self, event):
		self.frames[self.nowFrame].controller.key(event)

	def keyRelease(self, event):
		self.frames[self.nowFrame].controller.keyRelease(event)

	def mouse(self, event):
		self.frames[self.nowFrame].controller.mouse(event)
