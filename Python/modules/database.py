import csv
from time import time
import shutil
import os.path

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
		return (self.x, self.y, self.z, self.alpha, self.dist, self.id)
	
	def save (self,t,x,y,z,flag, alpha, dist):
		if (((self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2 > self.deltaR**2) or flag == True):
			
			print('Saving: ',t,' ', x,' ',y,' ',z,' ', flag)
			self.writer.writerow(localize_floats([t,x,y,z,flag]))
			
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
def localize_floats(row):
		return [
        str(el).replace('.', ',') if isinstance(el, float) else el 
        for el in row
		]