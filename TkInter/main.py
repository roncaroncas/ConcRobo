from mods.gui import GUI
from mods.network import Ethernet, FakeConnect
from mods.state import State
from mods.config import *

import os


class Server:

	######## SETUP
	def __init__(self):
		self.state = State(self)
		self.gui = GUI(self)
		self.conex = FakeConnect()

		print(self.state)

	######### REFRESH DO GUI
	def updateGUI(self):
		self.gui.update(self.state)

	######### CONTROLLERS

	#### CONNECTION SETUP:

	def testConnection(self):

		names = ["Router", "Zinho ", "CAM1   ", "CAM2   "]
		IPs = [IP_ROUTER, IP_ZINHO, IP_CAM1, IP_CAM2]
		responses = []

		for i in range (4):
			if os.system("ping -n 1 -w 20 {}".format(IPs[i])) == 0:
				responses.append(("{}\t{}\tOK!").format(names[i], IPs[i]))
			else:
				responses.append(("{}\t{}\tFAIL").format(names[i], IPs[i]))

		self.gui.frames['SetupConnectView'].t_p_router.set(responses[0])
		self.gui.frames['SetupConnectView'].t_p_zinho.set(responses[1])
		self.gui.frames['SetupConnectView'].t_p_cam1.set(responses[2])
		self.gui.frames['SetupConnectView'].t_p_cam2.set(responses[3])


	def getLastID(self):
		''' Retorna o ultimo ID'''
		
		#TODO
		ID = 1
		
		self.gui.frames['SetupConnectView'].id.set("ID: {:04}".format(ID))
		self.gui.frames['SetupConnectView'].e_id['state'] = "disabled"
		
	def getNewID(self):
		'''Retorna o próximo ID livre'''
		
		#TODO
		ID = 2

		self.gui.frames['SetupConnectView'].id.set("ID: {:04}".format(ID))
		self.gui.frames['SetupConnectView'].e_id['state'] = "disabled"

	def customID(self):
		self.gui.frames['SetupConnectView'].e_id['state'] = "normal"
		
	def connect(self):
		'''Tenta conectar com o Zinho e retorna True se conseguiu, False se não conseguiu
		Além disso, cria-se um database com o referido id
		'''

		#TODO

		ID = self.gui.frames['SetupConnectView'].id.get()
		
		success = True
		if success:
			self.gui.show_frame("ConnectView")
		else:
			self.gui.show_frame("StartView")


	#### Advanced


if __name__ == "__main__":
	zinho = Server()

	while True:
		zinho.gui.refresh(zinho.state)
		zinho.gui.update_idletasks()
		zinho.gui.update()