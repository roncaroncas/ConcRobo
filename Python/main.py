from time import sleep, time
from os import listdir
from mods.state import State
from mods.network import Ethernet, Serial, FakeConnect
from mods.protocol import Message, Response
from mods.database import DataBase
from mods.utils import *
from mods.config import *
from mods.gui import GUI

#pyinstaller main.py -F -w
	
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
				

		self.db = None
				
		#VARIAVEL DE FLUXO: Alternar entre mandar write de client -> arduino e pedir read de client -> arduino
		self.writeTurn = True #altera-se entre true e false para enviar informacoes de movimento ou para pedir informacoes analogicas
		
			
	
	def getInput(self,tela):
		key, clicked, flag = self.gui.getAction(tela)
		#print(tela, key, clicked, flag)
		return (key, clicked, flag)
		
	def doStartAction(self, state, key, clicked, flag):
		
		tela = "Start"	
		#Flags
		if flag == "quit":
			tela = "Quit"
			
		#START SCREEN
		#MOUSE:
		elif clicked == "connect":
			state.state['message'] = 'Conectando...'
			self.gui.update('Start', state.state)
			if self.conex.connect():
				#Cria um novo db
				self.db = DataBase(state.state['newRoute'])
				p = self.db.params() #[id, x, y, z, alph, dist, listX, listY]
				state = State(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
				tela = 'Connected'
				state.state['message'] = ''
			else:
				state.state['message'] = 'Conexão Falhou!'
				
		elif clicked == 'help':
			tela = 'Help'
		elif clicked == 'routeSwitch':
			state.state['newRoute'] = not(state.state['newRoute'])
		
		return (tela, state)
				
	def doConnectedAction(self, state, key, clicked, flag):
		
		tela = "Connected"
		
		#Flags
		if flag == "quit":
			tela = "Quit"
			
		#CONNECTED SCREEN	
		#priority actions
		elif key == 'ESCAPE':
			self.conex.disconnect()
			tela = 'Start'
			self.db.save(time(),state.state['x0'], state.state['y0'], state.state['z0'], state.state['alpha'], state.state['distance'], state.state['flag'])
			self.db.close()
		#WRITE TURN:
		elif (self.writeTurn):
			self.writeTurn = False
			self.msg.key2data(key)
		#READ TURN
		else:
			self.writeTurn = True
			self.msg.anyInfo()
			
		#process message	
		if tela == "Connected":

			tic = time()
		
			#sendMsg (msg -> )
			tela, state = self.sendMsg(state, self.msg)
			
			#print(self.msg)

			#getResp (server -> resp)
			self.getResp(state)
			toc = time()

			ping = 1000*(toc-tic)
			state.state['ping'] = ping
			
			saved = self.db.save(toc, state.state['x0'], state.state['y0'], state.state['z0'], state.state['alpha'], state.state['distance'], state.state['flag'])
				
			if not (saved is None):
				state.state['listX'].append(saved[0])
				state.state['listY'].append(saved[1])
		
		return (tela, state)
			
			
	def doHelpAction(self, state, key, clicked, flag):
		
		tela = "Help"
		
		if flag == "quit":
			tela = "Quit"
			
		#MOUSE:
			#EMPTY
		#KEYBOARD:
		elif key == 'ESCAPE':
			self.conex.disconnect()
			tela = 'Start'
		
		return (tela, state)
				
	def sendMsg(self, state, msg):
		tela = "Connected"
		
		if not (self.conex.sendMsg(msg)):
			tela = "Start"
			state.state['message'] = "A Conexão caiu..."
			
		return (tela, state)
				
	
	def getResp(self,state):
		#pega-se tem resp da conexao
		success, resp = self.conex.getResp()
		
		if success:
			#altera-se o valor de resp de acordo com o que foi recebido
			self.resp.setData(resp)
		
			#guarda a resp no st
			self.storeResp(state)
		
		else:
			print("DISCONNECTING")
			self.st.state['message'] = "A Conexão caiu..."
			self.conex.disconnect()
			
		return success

	def storeResp(self,state):
		respData = self.resp.data
		respI = respData[0:1]
		respVal = respData[1:3]
		state.store(respI, respVal)
		return (state)


	def main(self):
	
		tela = "Start"
		
		percursos = listdir('./percursos')
		id = 0
		for p in percursos:
			print(p)
			if (p != "backup.csv"):
				if (int(p.split('.csv')[0]) > id):
					id = int(p.split('.csv')[0])
		
		state = State(id)
		
		print(state)
		
		while (tela != "Quit"):
			#print(state)

			#Atualiza os gráficos
			self.gui.update(tela, state.state)
			#print(state)
			
			# Le o input do usu?rio
			key, click, flag = self.getInput(tela) 
			
			# processa inputs
			if tela == "Start":
				tela, state = self.doStartAction(state, key, click, flag)
			elif tela == "Connected":
				tela, state = self.doConnectedAction(state, key, click, flag)
			elif tela == "Help":
				tela, state = self.doHelpAction(state, key, click, flag)
				
		self.conex.disconnect()


if __name__ == "__main__":
	Client().main()
