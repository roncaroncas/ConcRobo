from PIL import Image, ImageTk

class ConnectController:
	def __init__(self, server):
		self.server = server
		self.name = self.__class__.__name__.split("Controller")[0]
		
	def key(self, event):
		print ("clicked at", event.x, event.y)

	def mouse(self, event):
		print ("pressed", repr(event.char))

	def refresh(self, model):

		frame = self.server.gui.frames[self.name]
		
		#Atualiza ID/NOME
		frame.var_id.set("ID " + str(model.state['id']))

		#Atualiza Ping
		frame.var_ping.set("Ping: " + str(model.state['ping']))

		#Atualiza Move
		frame.varIm_move = ImageTk.PhotoImage(frame.images['moves']['N'])
		frame.varLb_move.configure(image=frame.varIm_move)

		#Atualiza X, Y e Z
		frame.var_x.set(str(model.state['x']))
		frame.var_y.set(str(model.state['y']))
		frame.var_z.set(str(model.state['z']))

		#Atualiza Angle A e B
		bg = frame.images['angles']['angleBG']
		angleA = frame.images['angles']['angleA'].rotate(model.state['angleA'])
		angleB = frame.images['angles']['angleB'].rotate(model.state['angleB'])

		frame.varIm_angleA = ImageTk.PhotoImage(Image.alpha_composite(bg, angleA))
		frame.varLb_angleA.configure(image=frame.varIm_angleA)
		frame.varIm_angleB = ImageTk.PhotoImage(Image.alpha_composite(bg, angleB))
		frame.varLb_angleB.configure(image=frame.varIm_angleB)

		#Atualiza Temp
		frame.var_temp.set(str(model.state['temperature']))
		#TODO: ATUALIZAR IMAGEM

		#Atualiza Pressao
		frame.var_pres.set(str(model.state['pressure']))
		#TODO: ATUALIZAR IMAGEM

		#Atualiza BatV BatA
		frame.var_batV.set(str(model.state['batteryV']))
		frame.var_batA.set(str(model.state['batteryA']))
		#TODO: ATUALIZAR IMAGEM
		
		#Atualiza Dist
		frame.var_dist.set(str(model.state['distance']))
		#frame.var_dist.set(1000.0)
		#TODO: ATUALIZAR IMAGEM

		#Atualiza Vel
		frame.var_vel.set(str(model.state['velocity']))