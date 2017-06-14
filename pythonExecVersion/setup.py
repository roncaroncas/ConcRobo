from distutils.core import setup
import os
from fnmatch import fnmatch
import py2exe

root = r'C:\Users\victor_roncalli\Documents\Concremat\Zinho\ConcRobo\pythonExecVersion'

data_files = [
	]
	
#####IMAGES in DATA_FILES
rootImg = root + '\img' 				#AJUSTAR ROOT!
pattern = "*.jpeg"

for path, _, files in os.walk(rootImg):
	_, folderName = os.path.split(path)
	imgFolder = ('img/'+folderName, [])
	for name in files:
		if fnmatch(name, pattern):
			imgFolder[1].append(os.path.join(path, name))
		data_files.append(imgFolder)



#######

###### dbConfig

rootConfig = root + '\config'
pattern = "*.csv"

for path, _, files in os.walk(rootConfig):
	configFolder = ('config', [])
	for name in files:
		if fnmatch(name, pattern):
			configFolder[1].append(os.path.join(path, name))
		data_files.append(configFolder)

#######

####### historico

data_files.append(('historico',[]))



for elem in data_files:		
	print(elem)

setup(
	name = "Zinho",
	data_files=data_files,
	windows=['main.py'],
	options={
		'py2exe': {
			'includes': ['mods'],
			'packages' :['mods'],
			'dist_dir' : r'C:\Users\victor_roncalli\Documents\Concremat\Zinho\ConcRobo\pythonExecVersion\distTest',
			'bundle_files' : 1,
		}
	}
)


