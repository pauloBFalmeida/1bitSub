import pygame
from movement import Movement
from fade import Fade

class Enemy(Movement, Fade):
	def __init__(self, x, y, type, color, size, time_fade, sub):
		self.type = type
		self.size = size
		self.sub = sub
		max_speed, accel, decel, self.range, self.life = self.type_attributes(type, size)

		# Movement(x, y, max_speed, acceleration, decelerate)
		Movement.__init__(self, x, y, max_speed, accel, decel)
		#Fade(color, time_fade)
		Fade.__init__(self, color, time_fade, False)

	def take_damage(self):
		self.life -= 1
	def is_alive(self):
		return self.life > 0

	# max_speed, accel, decel, range, life
	def type_attributes(self, type, size):
		if  type == 0:	#boss
			self.size = self.size * 4
			return (1, 0.105, 0.955, self.size, 3)
		elif type == 1:	# fast one
			return (2, 0.12, 0.98, size*1, 1)
		elif type == 2:	# normal
			return (1.8, 0.105, 0.955, size*2, 1)
		else:# type 3	# slow
			return (1.5, 0.105, 0.945, size*3, 1)

	def calc_direction(self):
		x_speed = 1 if (self.sub.x - self.x) > 0 else -1
		y_speed = 1 if (self.sub.y - self.y) > 0 else -1
		return (x_speed, y_speed)

	def update(self):
		x_speed, y_speed = 0,0
		x_speed, y_speed = self.calc_direction()
		Movement.accelerate(self, x_speed, y_speed)
		Movement.update(self)
		Fade.update(self)


	def render(self, window):
		x = self.x - self.size/2
		y = self.y - self.size/2
		pygame.draw.rect(window, self.color, (x, y, self.size, self.size))
		pygame.draw.rect(window, (255,0,0), (self.x, self.y, 1, 1))	# test
