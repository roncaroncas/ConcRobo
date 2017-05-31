from time import sleep, time
from state import State
from gui import GUI
from network import Ethernet, Serial, FakeConnect
from protocol import Message, Response
from database import DataBase
from utils import *
from config import *
	
class Client():
	
	def __init__(self):
		#DEFINE O TIPO DE CONEXAO:
		if CONEX == "OFFLINE":
			self.conex = FakeConnect()
		elif CONEX == "ETHERNET":
			self.conex = Ethernet()	   
		elif CONEX == "SERIAL":
			self.conex = Serial()
		else:
			print("Wrong Connection type!")
			
		#DEFINE OS OBJETOS NECESSARIOS
		self.msg = Message()
		self.resp = Response()
		self.gui = GUI()
		self.st = State()
		self.db = DataBase()
		
		#VARIAVEL DE FLUXO: Alternar entre mandar write de client -> arduino e pedir read de client -> arduino
		self.writeTurn = True #altera-se entre true e false para enviar informacoes de movimento ou para pedir informacoes analogicas
		
		self.tela = "Start"
		
		
	def getInput(self):
			
		keysBool, clickedButton, flag = self.gui.getAction(self.tela)
		key = keysBool2key(keysBool)
		
		print(self.tela, key, clickedButton, flag)
		
		#Flags
		if flag == "quit":
			self.tela = "Quit"
			return
	
		#START SCREEN
		if self.tela == "Start":
			#MOUSE:
			if clickedButton == "connect":
				self.st.state['message'] = 'Connecting...'
				self.gui.update(self.tela, self.st.state)
				if self.conex.connect():
					self.tela = 'Connected'
					self.st.state['message'] = ''
					return
				else:
					self.st.state['message'] = 'Connection Fail!'
					return
			elif clickedButton == 'help':
				self.tela = 'Help'
				return
			#KEYBOARD:
				#EMPTY
			
		#CONNECTED SCREEN
		elif self.tela == "Connected":
			
			#WRITE TURN:
			if (self.writeTurn):
				self.writeTurn = False
				#MOUSE:
					#EMPTY
				#KEYBOARD:
				if key == 'ESCAPE':
					self.conex.disconnect()
					self.tela = 'Start'
					return
				else:
					self.msg.key2data(key)
					return
			#READ TURN
			else:
				self.writeTurn = True
				self.msg.anyInfo()
				return
			
		#HELP SCREEN
		elif self.tela == "Help":
			#MOUSE:
				#EMPTY
			#KEYBOARD:
			if key == 'ESCAPE':
				self.conex.disconnect()
				self.tela = 'Start'
				return
				
	def sendMsg(self):
		if not (self.conex.sendMsg(self.msg)):
			self.tela = "Start"
			self.st.state['message'] = "Perdeu conexao!"
				
	
	def getResp(self):
		#pega-se tem resp da conexao
		success, resp = self.conex.getResp()
		
		if success:
			#altera-se o valor de resp de acordo com o que foi recebido
			self.resp.setData(resp)
		
			#guarda a resp no st
			self.storeResp()
		
		else:
			print("DISCONNECTING")
			self.st.state['message'] = "Perda de Conexao"
			self.conex.disconnect()
			
		return success

	def storeResp(self):
		respData = self.resp.data
		respI = respData[0:1]
		respVal = respData[1:3]
		self.st.store(respI, respVal)


	def main(self):
	
		while (self.tela != "Quit"):
		
			sleep(.10)
			print(self.st)

			#Atualiza os gráficos
			self.gui.update(self.tela, self.st.state)
			
			# Le o input do usu?rio (tambem considera uma possibilidade n?o haver nenhum)
			self.getInput() # processa inputs
					

			if self.tela == "Connected":

				tic = time()
			
				#sendMsg (msg -> )
				self.sendMsg()
				
				#print(self.msg)

				#getResp (server -> resp)
				self.getResp()
				toc = time()

				ping = 1000*(toc-tic)
				self.st.state['ping'] = ping
				
				self.db.save(toc,self.st.state['x0'], self.st.state['y0'], self.st.state['z0'], self.st.state['flag'])
					
			if (self.tela == "Quit"):
				self.conex.disconnect()


if __name__ == "__main__":
	Client().main()
