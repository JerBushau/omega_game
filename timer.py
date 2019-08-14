import pygame

class Timer:
	"""A generic frame based timer"""

	def __init__(self):
		self.now = 0
		self.is_active = False


	def start_timer(self):
		self.is_active = True
		self.now += 1


	def reset_timer(self):
		self.is_active = False
		self.now = 0


class Timer2:
	"""A generic timer"""

	def __init__(self, duration):
		self.started_at = 0
		self.duration = duration
		self.is_active = False
		self.is_repeating = False


	def set_duration(self, duration):
		self.duration = duration


	def start(self):
		self.is_active = True
		self.started_at = pygame.time.get_ticks()


	def start_repeating(self):
		self.is_repeating = True
		self.start()


	def reset(self):
		self.is_active = False
		self.is_repeating = False
		self.started_at = 0


	def is_finished(self):
		if self.is_active == False:
			return False
		now = pygame.time.get_ticks()
		timer_expired = now - self.started_at > self.duration
		is_finished = True if timer_expired else False
		
		if is_finished:
			if self.is_repeating:
				self.start_repeating()
			else: 
				self.reset()

		return is_finished