class ConnectView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		numColumns = 3
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)


		label_title = tk.Label(self, text="Instruções", font=gui.h1_font)
		label_title.grid(row=0,column=1)
		
		text = ("Para mover, use as teclas:\n"
			"	Q W E\n" 
			"	A S D\n" 
			"	Z X C\n\n"

			"Para voltar, aperte ESC\n\n" 

			"Você deve monitorar o Zinho\n"
			"e garantir condições seguras!\n\n"
						
			"Você tem acesso a:\n"
			" - Temperatura\n"
			" - Pressao\n"
			" - Inclinação\n"
			" - Tensão da Bateria,\n"
			" - Velocidade aproximada\n"
			" - Distancia percorrida\n\n"

			"Em relação a posição inicial,\n" 
			"XYZ representam respectivamente:\n"
			" - esquerda (-) ~ direita (+) \n"
			" - trás     (-) ~ frente  (+) \n"
			" - baixo    (-) ~ cima    (+)\n"
			 )
			
		label = tk.Label(self, text=text, font=gui.p_font, justify="left")
		label.grid(row=1,column=1)
		
		button = tk.Button(self, text="Voltar",
						   command=lambda: gui.show_frame("StartView"))
		button.grid(row=2,column=1)

	def refreshFrame(self, state):
		pass