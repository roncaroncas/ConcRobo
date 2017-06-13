import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pygame as pg
import pylab
import random as rnd

def make_fig(x,y):
    #Interface with matplotlib, draw plot on a given UI_Item "view"
	
	fig = pylab.figure(figsize=[4, 4], # Inches
                       dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                       )
    ax = fig.gca()
    ax.plot([rnd.random() for x in range(nb)])

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()

    #Create pygame surface from string
    surf = pg.image.fromstring(raw_data, size, "RGB")
	
	pylab.close(fig)
	
	return surface
	