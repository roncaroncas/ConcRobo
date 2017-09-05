import shutil
from os import listdir
from time import time
from win32api import MessageBox

class DataBase:
	def __init__(self, id):

		self.data = {
			#Parametros fixos
			'id':		id,
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
			'deltaR':	0.05, #distancia minima entre dois pontos em metros
		}

		self.csv = {
			'file':		None,
			'name':		None,
			'fail':		False,
		}

		self._ = {
			'i': 		0,
		}

		percursos = listdir('./percursos')
		idExiste = False
		for p in percursos:
			if (p != "backup.csv"):
				if (int(p.split('.csv')[0]) == int(id)):
					idExiste = True

		self.csv['name']	= "./percursos/"+ str(id) + ".csv"
		
		#SE O ID NAO EXISTE
		if not(idExiste):	
			self.csv['file'] = open(self.csv['name'], 'x', newline = '')
			self.csv['file'].write(';'.join(['t', 'x', 'y', 'z', 'alpha', 'dist', 'Flag'])+"\n")
			self.csv['file'].write(';'.join(str(elem).replace('.', ',') for elem in [0, self['x'], self['y'], self['z'], self['alpha'], self['dist'], "init"])+"\n")
			
		#SE O ID EXISTE
		else:		

			try:
				self.csv['file'] = open(self.csv['name'], 'a', newline = '')
			except:
				MessageBox(0, 'Feche o arquivo csv', 'Error')
				self.csv['fail'] = True
				return
				
			p = self.paramsFromFile()
			
			self['x'] 		= p[0]
			self['y'] 		= p[1]
			self['z'] 		= p[2]
			self['alpha'] 	= p[3]
			self['dist'] 	= p[4]
			self.csv['file'].write(';'.join(str(elem).replace('.', ',') for elem in [0, self['x'], self['y'], self['z'], self['alpha'], self['dist'], "init"])+"\n")

	def __getitem__(self, key):
		return(self.data[key])

	def __setitem__(self, key, value):
		if key in list(self.data.keys()):
			self.data[key] = value
		else:
			print("!!!!!!!!!!!!!!!!There is no >>",key, "<< key!")
			1/0

	def paramsFromFile(self):
		
		self.csv['file'].close()
	
		with open(self.csv['name'], 'r') as percurso:
			row = percurso.readline().split(";") #header
			
			for row in percurso:
				row = row[:-1].split(";") #tirando o \n
				x = round(float(row[1].replace(',', '.')),3)
				y = round(float(row[2].replace(',', '.')),3)
				z = round(float(row[3].replace(',', '.')),3)
				alpha = round(float(row[4].replace(',', '.')),3)
				dist = round(float(row[5].replace(',', '.')),3)

		self.csv['file'] = open(self.csv['name'], 'a', newline = '')
							
		return (x, y, z, alpha, dist)
	
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

			self.csv['file'].write(';'.join(replaceDot2Comma(["{:.1f}".format(t),x,y,z,alpha,dist,str(flag)]))+"\n")
						
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
			shutil.copyfile(self.csv['name'], './percursos/backup.csv')  
		except:
			MessageBox(0, 'Feche o arquivo backup.csv\n(Não foi possível realizar o backup)', 'Error')
		self.csv['file'] = open(self.csv['name'], 'a', newline='')
		
	def close(self):
		self.csv['file'].close()
		
#Convete "." para "," nos floats para que o excel consiga plotar os gráficos 
def replaceDot2Comma(row):
		return [
		str(el).replace('.', ',') if isinstance(el, float) else el 
		for el in row
		]