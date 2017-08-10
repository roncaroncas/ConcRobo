from mods.gui import GUI
from mods.network import Ethernet, FakeConnect
from mods.state import State

import os

class Server:

	######## SETUP
	def __init__(self):
		self.state = State(self)
		self.gui = GUI(self)
		self.conex = FakeConnect()
		#self.config = ...

	######### REFRESH DO GUI
	def updateGUI(self):
		self.gui.update(self.state)

	######### CONTROLLERS

	#### CONNECTION SETUP:

	def testConnection(self):

		names = ["Router", "Zinho ", "CAM1   ", "CAM2   "]
		IPs = ["192.168.0.1", "192.168.0.125", "192.168.0.110", "192.168.0.10"]

		responses = []

		for i in range (4):
			if os.system("ping -n 1 -w 20 {}".format(IPs[i])) == 0:
				responses.append(("{}\t{}\tOK!").format(names[i], IPs[i]))
			else:
				responses.append(("{}\t{}\tFAIL").format(names[i], IPs[i]))

		return (responses)

	def getLastID(self):
		''' Retorna o ultimo ID'''
		
		#TODO

		return (1)

	def getNewID(self):
		'''Retorna o próximo ID livre'''
		
		#TODO

		return (2)

	def connect(self, ID):
		'''Tenta conectar com o Zinho e retorna True se conseguiu, False se não conseguiu
		Além disso, cria-se um database com o referido id
		'''

		#TODO

		return True


	#### Advanced

	def addOne(self):
		self.state.n += 1
		print(self.state)

class State:
	def __init__(self, server):
		self.n = 0
		self.server = server

	def __str__(self):
		return(str(self.n))


if __name__ == "__main__":
	zinho = Server()

	while True:
		zinho.gui.refresh(zinho.state)
		zinho.gui.update_idletasks()
		zinho.gui.update()