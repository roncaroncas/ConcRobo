#!/usr/bin/env python

'''
Esse programa é o cliente para operar o robô Zinho

-Arquitetura MVC+Network (Model-View-Controller)

-O programa funciona da seguinte maneira:
Tem-se um objeto principal, da classe Client.
Esse objeto cria dentro dele os seguintes objetos:
--- .controller
--- .gui (Graphical User Interfase -- Views)
--- .models
--- .conex
--- config

O programa funciona em um loop:
	loop:	
		client.sendMessage()			Se atender as condições, tentar enviar uma msg para o arduino
		client.receiveResponse()		Se atender as condições, Tenta receber uma mensagem do arduino
		client.updateRoute()			Se atender as condições, atualizar o arquivo csv do percurso
		client.updateGUI()				Se atender as condições, atualizar o view
		client.gui.update_idletasks() 	Se atender as condições, processar os processos na fila do GUI
		client.gui.update() 			Se atender as condições, atualiza o objeto gui


O controller é onde estão todas as funções que o computador deve processar, dividido em um arquivo para cada "pagina" do GUI,
inclusive aqui estão as regras para atualizar as imagens.

O Gui é onde estão descritos todos os objetos gráficos, como estão dispostas as páginas e ele é também relaciona os comandos do
usuário (mouse e teclado por exemplo) com o controller

O Models é onde estão as informações do usuário, do zinho e do percurso
-- user 	= (Move, id, name, flag)
-- zinho   	= (Move, Temperatura, pressao...)
-- route 	= (T, X, Y, Z, ...)

O conex é onde estão os métodos de comunicação entre o Client (esse programa) e o server (arduino do Zinho)

O config (em .json) é onde estão as configurações como IP_Zinho, IP_Router, Constantes de velocidade...

Mais detalhes sobre cada um desses itens estão nos arquivos de cada um deles.

######### GERAR O EXECUTAVEL ##############

Certifique-se que tem o python instalado e as seguintes bibliotecas:
-pyinstaller
-Pillow

(para instalar as bibliotecas, deve-se escrever no prompt de comando:
pip install pyinstaller pillow
)

Abra o prompt de comando do windows na pasta principal (que contém o arquivo Zinho.py (este arquivo))

pyinstaller -w Zinho.py

(-w = windowless)

Serão criados as pastas "build" e "dist", a pasta build pode ser descartada.
A pasta dist é de fato o Programa com o executável

Devem ser adicionada a pasta img dentro da pasta 'dist' para funcionar

Para executar, basta abrir o arquivo Zinho.exe que está dentro da pasta dist

############################################

Autor: Victor Roncalli
email: victor.roncalli.souza@gmail.com

'''

from controller import Controller
from views import GUI
from models import Models

from os import path, makedirs, listdir
import tkinter as tk
from tkinter import messagebox

import config

class Client:

	##################### SETUP ###################

	def __init__(self):

		#Carregando as variáveis globais do config
		config.init()
		print("CONFIG INICIALIZADO")

		#Carrega o Controller (as funções)
		self.controller = Controller(self)
		print("CONTRO INICIALIZADO")
	
		#Carrega o View (os gráficos)
		self.gui = GUI(self)
		print("GUI INICIALIZADO")

		#Carrega o Models (Zinho, User e Percurso)
		self.models = Models(self)
		print("MODELS INICIALIZADO")

		#Carrega a conexão
		self.controller.initCONEX()  #CRIA O self.conex
		print("CONEX INICIALIZADO")


		#variaveis de fluxo
		self.writeTurn = True
		self.cont = True

	def __str__(self):
		return str(self.model)


	##################### UPDATE ##################

	#Update Database	
	def updateRoute(self):
		if self.models['Route'] != None:
			self.models['Route'].save(self.models)

	#update GUI
	def updateGUI(self):
		self.gui.refreshAll(self.models)

	def on_exit(self):
		"""When you click to exit, this function is called"""
		self.gui.destroy()
		
		if self.models['Route'] != None:
			self.models['Route'].close()
		
		if self.conex:
			self.conex.disconnect()
			
		self.cont = False


if __name__ == "__main__":
	client = Client()
	client.gui.wm_title("Zinho 3.0")

	while client.cont:
		client.conex.sendMessage()
		client.conex.receiveResponse()
		client.updateRoute()
		client.updateGUI()
		if client.cont:
			client.gui.update_idletasks()
		if client.cont:
			client.gui.update()
