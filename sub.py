import pygame
from movement import Movement
from fade import Fade

class Sub(Movement, Fade):
	def __init__(self, x, y, color, size, time_fade, range):
		self.size = size
		self.range = range
		# Movement(x, y, max_speed, acceleration, decelerate)
		Movement.__init__(self, x, y, 1.8, 0.105, 0.955)
		#Fade(color, time_fade, start_fadein)
		Fade.__init__(self, color, time_fade, True)
		# statistics
		self.time = 0
		self.sec = 0
		self.kills = 0
		self.bombs = 0

	def add_bomb(self):
		self.bombs += 1
	def add_elimination(self):
		self.kills += 1

	def update(self):
		Movement.update(self)
		Fade.update(self)
		self.time += 1
		if self.time == 60:
			self.time = 0
			self.sec += 1

	def render(self, window):
		x = self.x - self.size/2
		y = self.y - self.size/2
		pygame.draw.rect(window, self.color, (x, y, self.size, self.size))
