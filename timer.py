
class Timer:
	"""A generic timer"""

	def __init__(self):
		self.now = 0
		self.is_active = False


	def start_timer(self):
		self.is_active = True
		self.now += 1


	def reset_timer(self):
		self.is_active = False
		self.now = 0