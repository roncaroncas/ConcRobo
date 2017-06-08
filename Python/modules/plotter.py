import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pygame
from pygame.locals import *


import matplotlib.backends.backend_agg as agg

import pylab

class Plotter:
	def __init__(self):
		pass
				   
		
	def get_surface(self, x, y):
		self.fig = pylab.figure(figsize=[4, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
		
		line, = plt.plot(x, y, '-')
		print(a)
		input()
		a.axis([0, 6, 0, 20]) 
		
		print(a)
		pass
		
		self.axis = self.fig.gca()
		print(self.axis)
		self.axis.plot(x,y)
		
		canvas = agg.FigureCanvasAgg(self.fig)
		canvas.draw()
		renderer = canvas.get_renderer()
		raw_data = renderer.tostring_rgb()

		size = canvas.get_width_height()
		
		surf = pygame.image.fromstring(raw_data, size, "RGB")
		
		return surf
				