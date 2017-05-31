import csv
from time import time
class DataBase:
	def __init__(self):
		self.fileName = "DataBase/"+str(time()) + ".csv"
	
		self.csv = open(self.fileName, 'x', newline='')
		self.writer = csv.writer(self.csv, delimiter=';')
		self.writer.writerow(['t','x','y','z','Flag'])
	
	def save (self,t,x,y,z,flag):
		print('Saving: ',t,' ', x,' ',y,' ',z,' ', flag)
		self.writer.writerow(localize_floats([t,x,y,z,flag]))
		
	def close(self):
		self.close()
		
def localize_floats(row):
		return [
        str(el).replace('.', ',') if isinstance(el, float) else el 
        for el in row
		]