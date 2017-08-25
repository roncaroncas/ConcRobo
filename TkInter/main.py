from controller import Controller
from views import GUI
from mods.network import Ethernet, FakeConnect
from models import Models
from mods.database import DataBase
from config import *

from os import path, makedirs, listdir

import tkinter as tk
from tkinter import messagebox

import os

class Server:

	##################### SETUP ###################

	def __init__(self):
		self.controller = Controller(self)
		self.gui = GUI(self)
		self.models = Models(self)
		self.db = None

		print(CONEX)

		if CONEX == "ETHERNET":
			self.conex = Ethernet(self)
		elif CONEX == "OFFLINE":
			self.conex = FakeConnect(self)
		else:
			print("CONNECTION ERROR!")
			
		#variavel de fluxo
		self.writeTurn = True

		#Cria pasta de Percursos caso ela nao exista
		if not(path.isdir('./percursos')):
			makedirs('./percursos')

	def __str__(self):
		return str(self.model)

	def initDB(self):
		self.db = DataBase(self.models['User']['id'])

	def initZinho(self):
		#Pega os parâmetros do Db criado
		p = self.db.paramsFromFile() #[id, x, y, z, alph, dist, perc]		
		self.models['Zinho'].__init__(p[0], p[1], p[2], p[3], p[4])
			

	##################### UPDATE ##################

	def sendMsg(self):
		if self.conex.connected == True:
			self.conex.sendMsg()

	def rcvResp(self):
		if self.conex.connected == True:
			self.conex.rcvResp()


	#update Database	
	def updateDB(self):
		if self.db != None:
			self.db.save(self.models)

	#update Model
	def updateModel(self):
		# self.models['User']['move'] = 
		#print(self.models['User'])
		pass

	#update GUI
	def updateGUI(self):
		self.gui.refreshAll(self.models)


if __name__ == "__main__":
	server = Server()

	while True:
		server.sendMsg()
		server.rcvResp()
		server.updateDB()
		server.updateModel()
		server.updateGUI()
		server.gui.update_idletasks()
		server.gui.update()
