from controller import Controller
from views import GUI
from mods.network import Ethernet, FakeConnect
from mods.model import Model
from mods.database import DataBase
from mods.config import *

from os import path, makedirs, listdir

import tkinter as tk
from tkinter import messagebox

import os


class Server:

	##################### SETUP ###################

	def __init__(self):
		self.controller = Controller(self)
		self.gui = GUI(self)
		self.conex = FakeConnect()
		self.model = Model()
		self.db = None

		#variavel de fluxo
		self.writeTurn = True

		#Cria pasta de Percursos caso ela nao exista
		if not(path.isdir('./percursos')):
			makedirs('./percursos')

	def __str__(self):
		return str(self.model)

	def createDB(self):
		self.db = DataBase(self.model.state['id'])

	def createModel(self):
		#Pega os parâmetros do Db criado
		p = self.db.params() #[id, x, y, z, alph, dist, perc]		
		self.model = Model(p[0], p[1], p[2], p[3], p[4], p[5], p[6])
			

	##################### UPDATE ##################

	#update Database	
	def updateDB(self):
		pass

	#update Model
	def updateModel(self):
		pass

	#update GUI
	def updateGUI(self):
		self.gui.refreshAll(self.model)


if __name__ == "__main__":
	zinho = Server()

	while True:
		zinho.updateDB()
		zinho.updateModel()
		zinho.updateGUI()
		zinho.gui.update_idletasks()
		zinho.gui.update()
