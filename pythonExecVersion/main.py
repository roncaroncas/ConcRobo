from time import sleep, time
import csv
from mods.state import State
from mods.network import Ethernet, Serial, FakeConnect
from mods.protocol import Message, Response
from mods.database import DataBase
from mods.utils import *
from mods.config import *
#from mods.gui import GUI
	
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
		
		with open ('config/dbControl.csv', 'r') as dbControl:
			dbConfig = {}
			reader = csv.reader(dbControl, delimiter=';')
			for row in reader:
				if len(row) == 2:
					dbConfig[row[0]] = row[1]
			#print(dbConfig)
		
		id = int(float(dbConfig['id']))
		self.st.state['id'] = id
		
		#self.db = DataBase(new=True)
		#p = self.db.params() #[x, y, z, alph, dist,id]
		#self.st = State(p[0], p[1], p[2], p[3], p[4], p[5])
		
		
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
					#Cria um novo db
					self.db = DataBase(self.st.state['id']+self.st.state['newRoute'])
					p = self.db.params() #[x, y, z, alph, dist, id, listX, listY]
					print("PPPPPPPPPPPPPPPPPP", p)
					self.st = State(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
		
					self.tela = 'Connected'
					self.st.state['message'] = ''
					return
				else:
					self.st.state['message'] = 'Connection Fail!'
					return
			elif clickedButton == 'help':
				self.tela = 'Help'
				return
			elif clickedButton == 'routeSwitch':
				self.st.state['newRoute'] = not(self.st.state['newRoute'])
				return
			#KEYBOARD:
				#EMPTY
			
		#CONNECTED SCREEN
		elif self.tela == "Connected":
			
			#priority actions
			if key == 'ESCAPE':
				self.conex.disconnect()
				self.tela = 'Start'
				return
			
			#WRITE TURN:
			if (self.writeTurn):
				self.writeTurn = False
				#MOUSE:
					#EMPTY
				#KEYBOARD:
					#EMPTY
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
			#print(self.st)

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
				
				saved = self.db.save(toc,self.st.state['x0'], self.st.state['y0'], self.st.state['z0'], self.st.state['flag'], self.st.state['alpha'], self.st.state['distance'])
					
				if not (saved is None):
					self.st.state['listX'].append(saved[0])
					self.st.state['listY'].append(saved[1])
					
			if (self.tela == "Quit"):
				self.conex.disconnect()


if __name__ == "__main__":
	Client().main()
