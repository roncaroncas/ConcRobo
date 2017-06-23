import shutil
from os import listdir
from time import time

class DataBase:
	def __init__(self, new=True):
		
		self.deltaR = 0.05 #distancia minima entre dois pontos em metros
		self.i = 0
		
		percursos = listdir('./percursos')
		id = 0
		for p in percursos:
			print(p)
			if (p != "backup.csv"):
				if (int(p.split('.csv')[0]) > id):
					id = int(p.split('.csv')[0])
		if new:
			id += 1
				
		self.fileName = "percursos/"+ str(id) + ".csv"
		
		#SE O ID NAO EXISTE
		if new:
		
			self.id = id
			
			self.x = 0
			self.y = 0
			self.z = 0
		
			self.alpha = 90
			self.dist = 0
			
			self.csvFile = open(self.fileName, 'x', newline = '')
			self.csvFile.write(';'.join(['t', 'x', 'y', 'z', 'alpha', 'dist', 'Flag'])+"\n")
			self.csvFile.write(';'.join(str(elem) for elem in [time(), self.x, self.y, self.z, self.alpha, self.dist, True])+"\n")
				
		#SE O ID EXISTE
		else:
			self.csvFile = open(self.fileName, 'a', newline = '')
			
			self.id = id
					
			p = self.params()
			
			self.id = id
			self.x = p[1]
			self.y = p[2]
			self.z = p[3]
			self.alpha = p[4]
			self.dist = p[5]
					
	def params(self):
		
		listX = []
		listY = []
		
		self.csvFile.close()
	
		with open(self.fileName, 'r') as percurso:
			row = percurso.readline().split(";") #header
			
			for row in percurso:
				row = row[:-1].split(";") #tirando o \n
				x = float(row[1].replace(',', '.'))
				y = float(row[2].replace(',', '.'))
				z = float(row[3].replace(',', '.'))
				alpha = float(row[4].replace(',', '.'))
				dist = float(row[5].replace(',', '.'))
				listX.append(x)
				listY.append(y)
				#print(x,y,z)	
			
		if not(listX):
			listX = [0]
		if not(listY):
			listY = [0]
			
		self.csvFile = open(self.fileName, 'a', newline = '')
								
		return (self.id, x, y, z, alpha, dist, listX, listY)
	
	def save (self,t,x,y,z, alpha, dist, flag):
		if (((self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2 > self.deltaR**2) or flag == True):
			
			self.csvFile.write(';'.join(replaceDot2Comma([t,x,y,z,alpha,dist,str(flag)]))+"\n")
						
			self.x = x
			self.y = y
			self.z = z
			
			self.alpha = alpha
			self.dist = dist
			
			self.i += 1
			if self.i%20 == 0:
				self.backup()
				
			return (self.x, self.y)
			
		return None
		
	
	def backup(self):
		#fecha o csv, copia e reabre.
	
		self.csvFile.close()
		try:
			shutil.copyfile(self.fileName, 'percursos/backup.csv')  
		except:
			print("Backup Fail")
		self.csvFile = open(self.fileName, 'a', newline='')
		
	def close(self):
		self.csvFile.close()
		
#Convete "." para "," nos floats para que o excel consiga plotar os gráficos 
def replaceDot2Comma(row):
		return [
        str(el).replace('.', ',') if isinstance(el, float) else el 
        for el in row
		]