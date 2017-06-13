import csv
import shutil
import os.path
#from .plotter import Plotter

class DataBase:
	def __init__(self, id, new=True):
		
		self.deltaR = 0.05 #distancia minima entre dois pontos em metros
		
		self.i = 0
		
		self.fileName = "historico/"+ str(id) + ".csv"
		
		#SE O ID JA EXISTE:
		if os.path.isfile(self.fileName):
			self.csv = open(self.fileName, 'a', newline='')
			self.writer = csv.writer(self.csv, delimiter=';')
			
			with open ('config/dbControl.csv', 'r') as dbControl:
				dbConfig = {}
				reader = csv.reader(dbControl, delimiter=';')
				for row in reader:
					if len(row) == 2:
						dbConfig[row[0]] = row[1]
				print(dbConfig)
				
			self.id = id
		
			self.x = float(dbConfig['x'])
			self.y = float(dbConfig['y'])
			self.z = float(dbConfig['z'])
			
			self.alpha = float(dbConfig['alpha'])
			
			self.dist = float(dbConfig['dist'])
			
			#self.plot = Plotter()

			
		#SE O ID NAO EXISTE
		else:
			self.csv = open(self.fileName, 'x', newline='')   #TROCAR 'w' por 'x' para nao dar overwrite
			self.writer = csv.writer(self.csv, delimiter=';')
			self.writer.writerow(['t','x','y','z','Flag'])
			
			self.id = id
		
			self.x = 0
			self.y = 0
			self.z = 0
		
			self.alpha = 90.0
		
			self.dist = 0
			
				
		#Atualiza o config.csv
		with open ('config/dbControl.csv', 'w') as dbControl:
			writer = csv.writer(dbControl, delimiter=';')
			writer.writerow([	'id',		str(self.id)  	])
			writer.writerow([	'x',		str(self.x)  	])
			writer.writerow([	'y',		str(self.y)  	])
			writer.writerow([	'z',		str(self.z)  	])
			writer.writerow([	'alpha',	str(self.alpha) ])
			writer.writerow([	'dist',		str(self.dist)  ])	
		
	def params(self):
		
		listX = []
		listY = []
		with open (self.fileName, 'r') as hist:
				reader = csv.reader(hist, delimiter=';')
				
				for row in reader:
					try:
						#print("TRYYYYING")
						print("FLLLLLLLAOAROARO: ", (row[1]))
						listX.append(float(row[1].replace(',', '.')))
						listY.append(float(row[2].replace(',', '.')))
					except:
						pass
				listX = listX[1:]
				listY = listY[1:]
				
				if not(listX):
					listX = [0]
				if not(listY):
					listY = [0]
				
		
		return (self.x, self.y, self.z, self.alpha, self.dist, self.id, listX, listY)
	
	def save (self,t,x,y,z,flag, alpha, dist):
		if (((self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2 > self.deltaR**2) or flag == True):
			
			#print('Saving: ',t,' ', x,' ',y,' ',z,' ', flag)
			self.writer.writerow(replaceDot2Comma([t,x,y,z,flag]))
			
			#print('Extras: alph: ',alpha,' dist: ',dist)
			
			self.x = x
			self.y = y
			self.z = z
			
			self.alpha = alpha
			self.dist = dist
			
			self.i += 1
			if self.i%100 == 0:
				self.backup()
				
			with open ('config/dbControl.csv', 'w') as dbControl:
				writer = csv.writer(dbControl, delimiter=';')
				writer.writerow([	'id',		str(self.id)  	])
				writer.writerow([	'x',		str(self.x)  	])
				writer.writerow([	'y',		str(self.y)  	])
				writer.writerow([	'z',		str(self.z)  	])
				writer.writerow([	'alpha',	str(self.alpha) ])
				writer.writerow([	'dist',		str(self.dist)  ])
				
			return (self.x, self.y)
			
		return None
			
	
	
	def backup(self):
		#fecha o csv, copia e reabre.
	
		self.csv.close()
		try:
			shutil.copyfile(self.fileName, 'backup/ultimo.csv')  
		except:
			print("Backup Fail")
		self.csv = open(self.fileName, 'a', newline='')
		self.writer = csv.writer(self.csv, delimiter=';')

		
#Convete "." para "," nos floats para que o excel consiga plotar os gráficos 
def replaceDot2Comma(row):
		return [
        str(el).replace('.', ',') if isinstance(el, float) else el 
        for el in row
		]
		