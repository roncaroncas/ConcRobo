import shutil
from os import listdir
from time import time
from win32api import MessageBox

class DataBase:
	def __init__(self, new=True):
		
		self.deltaR = 0.05 #distancia minima entre dois pontos em metros
		self.i = 0
		self.initTime = time()
		self.fail = False
		
		percursos = listdir('../percursos')
		id = -1
		for p in percursos:
			if (p != "backup.csv"):
				if (int(p.split('.csv')[0]) > id):
					id = int(p.split('.csv')[0])
		if new:
			id += 1		
			
		#SE O ID NAO EXISTE
		if new or id == -1:
		
			if id == -1:
				id = 0

			self.fileName = "../percursos/"+ str(id) + ".csv"

				
			self.id = id
			
			self.x = 0
			self.y = 0
			self.z = 0
			self.t = 0
		
			self.alpha = 90
			self.dist = 0
			
			self.csvFile = open(self.fileName, 'x', newline = '')
			self.csvFile.write(';'.join(['t', 'x', 'y', 'z', 'alpha', 'dist', 'Flag'])+"\n")
			self.csvFile.write(';'.join(str(elem) for elem in [0, self.x, self.y, self.z, self.alpha, self.dist, "init"])+"\n")
			
				
		#SE O ID EXISTE
		else:		
			self.id = id
			
			self.fileName = "../percursos/"+ str(id) + ".csv"
			try:
				self.csvFile = open(self.fileName, 'a', newline = '')
			except:
				MessageBox(0, 'Feche o arquivo csv', 'Error')
				self.fail = True
				return
				
			p = self.params()
			
			self.id = id
			self.t = p[0]
			self.x = p[1]
			self.y = p[2]
			self.z = p[3]
			self.alpha = p[4]
			self.dist = p[5]
			self.csvFile.write(';'.join(str(elem).replace('.', ',') for elem in [0, self.x, self.y, self.z, self.alpha, self.dist, "init"])+"\n")
					
	def params(self):
		
		perc = []
		
		self.csvFile.close()
	
		print(self.fileName)
	
		with open(self.fileName, 'r') as percurso:
			row = percurso.readline().split(";") #header
			
			for row in percurso:
				row = row[:-1].split(";") #tirando o \n
				x = round(float(row[1].replace(',', '.')),3)
				y = round(float(row[2].replace(',', '.')),3)
				z = round(float(row[3].replace(',', '.')),3)
				alpha = round(float(row[4].replace(',', '.')),3)
				dist = round(float(row[5].replace(',', '.')),3)
				flag = row[6]
				perc.append((x,y,flag))
				
		#if not(perc):
		#	perc = [(0,0,"init")]

		self.csvFile = open(self.fileName, 'a', newline = '')
							
		return (self.id, x, y, z, alpha, dist, perc)
	
	def save (self,state):
		t = time() - self.initTime
		x = state.state['x0']
		y = state.state['y0']
		z = state.state['z0']
		alpha = state.state['alpha']
		dist = state.state['distance']
		flag = state.state['flag']
		
	
		if (((self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2 > self.deltaR**2) or flag):
			
			self.csvFile.write(';'.join(replaceDot2Comma([t,x,y,z,alpha,dist,str(flag)]))+"\n")
						
			self.t = t
			self.x = x
			self.y = y
			self.z = z
			
			self.alpha = alpha
			self.dist = dist
			
			self.i += 1
			if self.i%20 == 0:
				self.backup()
				
			state.state['perc'].append((self.x,self.y,flag))
			
		return state
		
	
	def backup(self):
		#fecha o csv, copia e reabre.
	
		self.csvFile.close()
		try:
			shutil.copyfile(self.fileName, '../percursos/backup.csv')  
		except:
			MessageBox(0, 'Feche o arquivo backup.csv\n(Não foi possível realizar o backup)', 'Error')
		self.csvFile = open(self.fileName, 'a', newline='')
		
	def close(self):
		self.csvFile.close()
		
#Convete "." para "," nos floats para que o excel consiga plotar os gráficos 
def replaceDot2Comma(row):
		return [
        str(el).replace('.', ',') if isinstance(el, float) else el 
        for el in row
		]