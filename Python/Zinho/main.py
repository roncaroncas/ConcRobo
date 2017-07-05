from time import sleep, time
from os import listdir, remove, path, makedirs
from mods.state import State
from mods.network import Ethernet, FakeConnect
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
		#Pega a tecla, o botão e o flag do GUI
		key, clicked, flag = self.gui.getAction(tela)
		
		action = None
		if key:
			action = key
		elif clicked:
			action = clicked
		elif flag:
			action = flag
		
		return (action)
		
	def doStartAction(self, state, action):
		''' 
		### START SCREEN ###
		Atualiza os valores do state e tela, de acordo com os inputs
		(state, action) -> (tela, state)'''
		
		#Considerando que vai ter no máximo 1 ação a ser feita
		
		#Flags
		if action == "quit":
			tela = "Quit"
			
		#Keyboard
			#None
			
		#Mouse:
		elif action == "connect":
			
			state.state['message'] = 'Conectando...'
			
			#atualiza a imagem para aparecer a menssagem enquanto estiver procurando conexao
			self.gui.update('Start', state.state)
			
			#tenta conectar
			success = self.conex.connect()
			
			#Se conectou com sucesso
			if success:
				#Tenta criar um novo db (podendo aproveitar um antigo se necessário)
				self.db = DataBase(new=state.state['newRoute'])
				
				if (self.db.fail):
					tela = "Start"
					
				else:
					#Pega os parâmetros do Db criado
					p = self.db.params() #[id, x, y, z, alph, dist, perc]
					
					#Cria um novo state com os parametros necessários
					state = State(p[0], p[1], p[2], p[3], p[4], p[5], p[6])
					#Muda de tela
					tela = 'Connected'
					
			#Se não conseguiu conectar
			else:
				#Mensagem de erro
				state.state['message'] = 'Conexão Falhou!'
				tela = "Start"
				
		#Se apertar os outros botões para mudar de tela
		elif action == 'help':
			tela = 'Help'
		elif action == 'advanced':
			tela = 'Advanced'
			
		#Se apertar o switch de Novo percurso, trocar o state de nova rota entre True e False
		elif action == 'routeSwitch':
			state.state['newRoute'] = not(state.state['newRoute'])
			tela = "Start"
			
		else:
			#Caso não tenha ação, manter tela"
			tela = "Start"
		
		return (tela, state)
				
	def doConnectedAction(self, state, action):
		''' 
		### CONNECTED SCREEN ###
		Atualiza os valores do state e tela, de acordo com os inputs
		(state, action) -> (tela, state)'''	
		
		#variavel de fluxo
		keepConnect = True
		
		##Flags
		if action == "quit":
			tela = "Quit"
		
		##Mouse
		elif action == "flag":
			state.state['flag'] = 'flag'
			state = self.db.save(state)
			state.state['flag'] = ''
			tela = "Connected"
	
		elif action == 'zPlus':
			state.state['zoom'] /= 2
			tela = "Connected"
		elif action == 'zMinus':
			state.state['zoom'] *= 2
			tela = "Connected"
			
		##Keyboard
		
		#Priority
		elif action == 'ESCAPE':
			keepConnect = False
			
		#Communicate
		else:
			#Write Turn
			if (self.writeTurn and (action)):
				self.writeTurn = False
				data = self.msg.key2data(action)
			
			#Read Turn
			else:
				self.writeTurn = True
				data = self.msg.anyInfo()
		
			#tempo de referencia para o Ping
			now = time()
		
			#sendMsg (msg -> )
			keepConnect = self.conex.sendMsg(data)
		
			#Se a conexão é para ser mantida, tentar receber data do servidor
			if keepConnect:
				#getResp (server -> resp)
				keepConnect, data = self.conex.getResp()
		
		
				#Se a conexão é para ser mantida, processar data recebida do servidor
				if keepConnect:	
					#atualiza o valor de resp de acordo com o que foi recebido
					self.resp.setData(data[2:5])
					
					#guarda a resp no State	
					state = self.applyResp(state, self.resp)

					#Calculando e armazenando o ping no state
					ping = 1000*(time()-now)
					state.state['ping'] = ping
					
					#Perguntar para o db se ele deseja salvar esse estado, e caso verdadeiro, atualiza o listX e listY do state
					state = self.db.save(state)
					
					tela = "Connected"
			
		
		#Fechar conexão se necessário
		if not(keepConnect):
			self.conex.disconnect()
			tela = 'Start'
			state.state['ping'] = 0
			state.state['message'] = 'Desconectado'
			saved = self.db.save(state)
			self.db.close()
			
		
		return (tela, state)
			
	def doHelpAction(self, state, action):
		''' 
		### HELP SCREEN ###
		Atualiza os valores do state e tela, de acordo com os inputs
		(state, action) -> (tela, state)'''
		
		#Flags
		if action == "quit":
			tela = "Quit"
			
		#Mouse:
			#None
			
		#Keyboard:
		elif action == 'ESCAPE':
			self.conex.disconnect()
			tela = 'Start'
			
		else:
			tela = "Help"
			
		
		return (tela, state)	
	
	def doAdvancedAction(self, state, action):
		''' 
		### ADVANCED SCREEN ###
		Atualiza os valores do state e tela, de acordo com os inputs
		(state, action) -> (tela, state)'''
		
		#Flags
		if action == "quit":
			tela = "Quit"
			
		#MOUSE:
		elif action == 'clear':
			percursos = listdir('../percursos')
			for p in percursos:
				remove('../percursos/'+p)
			state.state['id'] = 0
			state.state['message'] = "Percursos Zerados"
			tela = "Start"
		
		#KEYBOARD:
		elif action == 'ESCAPE':
			self.conex.disconnect()
			tela = 'Start'
		
		else:
			tela = "Advanced"
			
		return (tela, state)
		
	
	def applyResp(self, state, resp):
		''' atualiza o state de acordo com a resp'''
		respI = resp.data[0:1]
		respVal = resp.data[1:3]
		state.store(respI, respVal)
		return (state)

	def main(self):
	
		#Define condição inicial
		tela = "Start"
		
		#Cria pasta de Percursos caso ela nao exista
		if not(path.isdir('../percursos')):
			makedirs('../percursos')

		#define o id como o ultimo id criado ou 0
		percursos = listdir('../percursos')
		id = 0
		for p in percursos:
			#print(p)
			if (p != "backup.csv"):
				if (int(p.split('.csv')[0]) > id):
					id = int(p.split('.csv')[0])
		
		#Cria uma variavel de estado com todos os valores default com exceção de id
		state = State(id)
				
		#Loop principal
		while (tela != "Quit"):

			#Atualiza os gráficos
			self.gui.update(tela, state.state)
			
			# Le o input do usuario
			#key, click, flag = self.getInput(tela)
			action = self.getInput(tela)
			
			if not(action == None):
				print(tela, action)

				
			# processa inputs
			if tela == "Start":
				tela, state = self.doStartAction(state, action)
			elif tela == "Connected":
				tela, state = self.doConnectedAction(state, action)
			elif tela == "Help":
				tela, state = self.doHelpAction(state, action)
			elif tela == "Advanced":
				tela, state = self.doAdvancedAction(state, action)
	
		#Fecha conexão se sair do loop
		self.conex.disconnect()


if __name__ == "__main__":
	Client().main()
