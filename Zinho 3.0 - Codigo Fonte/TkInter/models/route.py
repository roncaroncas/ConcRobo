
'''

Esse model cria e gerencia um registro de um percurso e salva esse registro em um arquivo .csv dentro de uma pasta chamada "percursos".

Assim, tem-se o histórico de todo o caminho percorrido


A estrutura desse csv é descrito a seguir:

As duas primeiras linhas correspondem a parâmetros fixos.

Ex:		ID 			NOME
		0012 		Tubulação da obra X 

A terceira linha em branco para separar

As demais linhas correspondem ao tempo, posição, ângulo, distância percorrida e uma mensagem
Ex:		t 		x 		y 		z 		alpha 		dist 		flag
		0		0		0		0		90			0			inicio
		1		0		5		0		90			5			
		...


'''

import shutil
from os import listdir, path, makedirs
from time import time
from win32api import MessageBox

class Route:

	'''
	Cria e gerencia um banco de dados em csv nomeado pelo ID correspondente a um percurso
	nesse csv, 

	Essa classe possui as seguintes funções:
		self.paramsFromFile() -> Id, Nome, ultimoX, ultimoY, ultimoZ, ultimoAlpha, ultimoDist
		self.save(models) -> None
		self.backup() -> None

	Obs: Ele salva os numeros no csv com separador de decimais em , (padrão excel)
		e trabalha com separador decimais em . (padrao python)


	'''


	def __init__(self, id="0000", name=""):
		'''define os parametros
		em .data estão os parâmetros principais
		em .config estão as configurações relacionadas ao gerenciamento do database
		em .csv estão o arquivo e os parâmetros dele
		em ._ estão os parâmetros de controle de fluxo'''


		#Cria pasta de Percursos caso ela nao exista
		if not(path.isdir('../percursos')):
			makedirs('../percursos')


		self.data = {
			#Parametros fixos
			'id':		id,
			'name':		name,
			'initTime':	time(),

			#Ultima linha
			't':		.0,
			'x':		.0,
			'y':		.0,
			'z':		.0,
			'alpha':	90.0,
			'dist':		.0,
		}

		self.config = {
			'deltaR':	0.10, #distancia minima entre dois pontos em metros
		}

		self.csv = {
			'file':		None,
			'name':		None,
			'fail':		False,
			'ativo':	(id!="0000"), #True se não for 00000
		}

		self._ = {
			'i': 		0,		#para o backup
		}



		if self.csv['ativo']:
			
			#Descobrindo se o ID já existe

			percursos = listdir('../percursos')
			idExiste = False
			for p in percursos:
				try: 
					int(p[:4])
					if id == p[:4]:
						idExiste = True
						if len(p) > 8:
							name = p[7:-4]
				except:
					pass


			if name:
				self.csv['name']	= "../percursos/"+ str(id) + " - " + name +".csv"
			else:
				self.csv['name']	= "../percursos/"+ str(id) + ".csv"

			
			#SE O ID NAO EXISTE
			if not(idExiste):	
				self.csv['file'] = open(self.csv['name'], 'x', newline = '')

				self.csv['file'].write(';'.join(['Id', 'Nome'])+"\n")
				self.csv['file'].write(';'.join([self['id'], self['name']])+"\n")

				self.csv['file'].write(';'.join("\n"))
				
				self.csv['file'].write(';'.join(['t', 'x', 'y', 'z', 'alpha', 'dist', 'Flag'])+"\n")
				self.csv['file'].write(';'.join(replaceDot2Comma([0, self['x'], self['y'], self['z'], self['alpha'], self['dist'], "inicio"]))+"\n")

			#SE O ID EXISTE
			else:		

				try:
					self.csv['file'] = open(self.csv['name'], 'a', newline = '')
				except:
					MessageBox(0, 'Feche o arquivo csv', 'Error')
					self.csv['fail'] = True
					return
					
				self.paramsFromFile()

				p = self.data
			
				self.csv['file'].write(';'.join(replaceDot2Comma([0, p['x'], p['y'], p['z'], p['alpha'], p['dist'], "inicio"]))+"\n")

	def __getitem__(self, key):
		return(self.data[key])

	def __setitem__(self, key, value):
		if key in list(self.data.keys()):
			self.data[key] = value
		else:
			raise("There is no >>",key, "<< key!")

	def paramsFromFile(self):

		'''Le os parâmetros fixos do database e os últimos x,y,z,alpha,dist'''
		
		self.csv['file'].close()
	
		with open(self.csv['name'], 'r') as percurso:

			#header dos parametros fixos
			row = percurso.readline()

			#parametros fixos
			row = percurso.readline()
			self.id, self.name = row[:-1].split(";") #tirando o \n

			#linha em branco
			row = percurso.readline() #blank line
			
			#header dos t,x,y,z,alpha,dist
			row = percurso.readline() #blank line
			
			#linhas com t,x,y,z,alpha,dist
			for row in percurso:
				row = row[:-1].split(";") #tirando o \n
				self['x'] = round(float(row[1].replace(',', '.')),3)
				self['y'] = round(float(row[2].replace(',', '.')),3)
				self['z'] = round(float(row[3].replace(',', '.')),3)
				self['alpha'] = round(float(row[4].replace(',', '.')),3)
				self['dist'] = round(float(row[5].replace(',', '.')),3)

		self.csv['file'] = open(self.csv['name'], 'a', newline = '')



	def save (self, models):
		
		zinho = models['Zinho']
		user = models['User']

		t = time() - self['initTime']
		x = zinho['x']
		y = zinho['y']
		z = zinho['z']
		alpha = zinho['alpha']
		dist = zinho['distance']

		flag = user['flag']
		
		if (((self['x']-x)**2 + (self['y']-y)**2 + (self['z']-z)**2 > self.config['deltaR']**2) or flag):
			
			user['flag'] = ""

			self.csv['file'].write(';'.join(replaceDot2Comma([t,x,y,z,alpha,dist,str(flag)]))+"\n")
						
			self['t'] = t
			self['x'] = x
			self['y'] = y
			self['z'] = z
			
			self['alpha'] = alpha
			self['dist'] = dist
			
			self._['i'] += 1
			if self._['i']%20 == 0:
				self.backup()		
	
	def backup(self):
		#fecha o csv, copia e reabre.
	
		self.csv['file'].close()
		try:
			shutil.copyfile(self.csv['name'], '../percursos/backup.csv')  
		except:
			MessageBox(0, 'Feche o arquivo backup.csv\n(Não foi possível realizar o backup)', 'Error')
		self.csv['file'] = open(self.csv['name'], 'a', newline='')
		
	def close(self):
		try:
			self.csv['file'].close()
		except:
			pass

#UTILS:
		
#Convete "." para "," nos floats para que o excel consiga plotar os gráficos 
def replaceDot2Comma(row):
		return [
		str(round(el,3)).replace('.', ',') if isinstance(el, float) else str(el) 
		for el in row
		]

def replaceComma2Dot(row):
		return [
		str(round(el,3)).replace('.', ',') if isinstance(el, float) else str(el) 
		for el in row
		]