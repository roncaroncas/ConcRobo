from .AdvancedController import AdvancedController
from .ConnectController import ConnectController
from .HelpController import HelpController
from .SetupConnectController import SetupConnectController
from .StartController import StartController

class Controller:
	def __init__(self, server):

		self.controls = {}

		for control_name in ("Start", "Connect", "SetupConnect", "Help", "Advanced"):
			control_class = eval(control_name+"Controller")
			controller = control_class(server)
			self.controls[control_name] = controller