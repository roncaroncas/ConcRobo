'''
O Controller é responsável por todas as funções relacionadas a interação com o usuário

Recomenda-se ler esse texto depois de ler a explicação de views/__init__.py

Esse arquivo funciona da seguinte maneira:
Gera-se um objeto Controller com um ponteiro ao Client

Cada uma dessas páginas deve estar em um arquivo separado onde cada uma delas possui um objeto com o nome "Frame+Controller",
o nome da pagina deve ser adicionado a variável chamada "paginas".
Cada Controller deve ter seu arquivo equivalente em View

Exemplo: A pagina menu deve estar organizada num arquivo "Menu.py" dentro da pasta "views" e deve possuir um objeto chamado "MenuView".
Além disso, deve haver um arquivo Menu.py na pasta controller com um objeto MenuController.

Esse arquivo chama todos os controller guardando no dicionário ".controls"

'''

from .Menu import MenuController
from .Conectar import ConectarController
from .Conectado import ConectadoController
from .Instrucoes import InstrucoesController
from .Configuracoes import ConfiguracoesController
from .Creditos import CreditosController

import config

from network import Ethernet, FakeConnect

#

class Controller:
	def __init__(self, client):

		self.controls = {}
		self.client = client

		paginas = ("Menu", "Conectar", "Conectado", "Instrucoes", "Configuracoes", "Creditos")

		# for control_name in ("Start", "Connect", "SetupConnect", "Help", "Advanced"):
		for control_name in paginas:
			control_class = eval(control_name+"Controller")
			controller = control_class(client)
			self.controls[control_name] = controller


	def initDB(self):
		self.client.models['Route'].__init__(id=self.client.models['User']['id'], name=self.client.models['User']['name'])

	def initZinho(self):
		#Pega os parâmetros do Db criado
		p = self.client.models['Route'].data #[id, x, y, z, alph, dist, perc]		
		self.client.models['Zinho'].__init__(x=p['x'], y=p['y'], z=p['z'], alpha=p['alpha'], dist=p['dist'])

	def initCONEX(self):
		if config.CONEX == "ETHERNET":
			self.client.conex = Ethernet(self.client)
		elif config.CONEX == "OFFLINE":
			self.client.conex = FakeConnect(self.client)
		else:
			raise("CONNECTION ERROR!")