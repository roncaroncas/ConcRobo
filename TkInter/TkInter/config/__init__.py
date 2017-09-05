# Esse arquivo importa as variáveis de um arquivo .json chamado "config.json" para variáveis no python.

# Caso esse .json nao exista, ele é criado automaticamente

import json

def init():

	global IP_ROUTER
	global IP_ZINHO
	global IP_CAM1
	global IP_CAM2

	global PORT_ZINHO
	global PORT_CAM1
	global PORT_CAM2

	global CONEX

	global Krv
	global Krw
	global Kdv
	global Kdw
	global Klv
	global Klw

	try:
		with open('./config.json') as jfile:
		            config = json.load(jfile)

		IP_ROUTER = config['IP_ROUTER']

		IP_ZINHO = config['IP_ZINHO']
		PORT_ZINHO = int(config['PORT_ZINHO'])

		IP_CAM1 = config['IP_CAM1']
		PORT_CAM1 = int(config['PORT_CAM1'])

		IP_CAM2 = config['IP_CAM2']
		PORT_CAM2 = int(config['PORT_CAM2'])
					
		CONEX = config['CONEX'] #MUST BE: OFFLINE OR ETHERNET


		#MOVEMENT CONSTANTS:
		## Movimento Reto:
		Krv = 	config['Krv']	#m/s
		Krw = 	config['Krw']	#voltas/s
		## Movimento Diagonal 
		Kdv = 	config['Kdv'] 	# m/s
		Kdw = 	config['Kdw'] 	# voltas/s
		## Movimento Lado
		Klv = 	config['Klv']	# m/s
		Klw = 	config['Klw'] 	# voltas/s

	except:

		data = {}

		data['IP_ROUTER'] = '192.168.0.1'

		data['IP_ZINHO'] = '192.168.0.120'
		data['PORT_ZINHO'] = '23'

		data['IP_CAM1'] = '192.168.0.10'
		data['PORT_CAM1'] = '34567'

		data['IP_CAM2'] = '192.168.0.110'
		data['PORT_CAM2'] = '34568'

		data['CONEX'] = "ETHERNET"

		data["Krv"] = 0.1125
		data["Krw"] = 0
		data["Kdv"] = 0.06081
		data["Kdw"] = 0.03226
		data["Klv"] = 0
		data["Klw"] = 0.06427	

		IP_ROUTER = '192.168.0.1'

		IP_ZINHO = '192.168.0.120'
		PORT_ZINHO = '23'

		IP_CAM1 = '192.168.0.10'
		PORT_CAM1 = '34567'

		IP_CAM2 = '192.168.0.110'
		PORT_CAM2 = '34568'

		CONEX = "ETHERNET"

		Krv = 0.1125
		Krw = 0
		Kdv = 0.06081
		Kdw = 0.03226
		Klv = 0
		Klw = 0.06427	

		with open('config.json', 'w') as f:
			json.dump(data, f)