import pygame
from movement import Movement
from fade import Fade
from atack import Atack

class Enemy(Movement, Fade, Atack):
	def __init__(self, x, y, type, color, size, time_fade, sec_div10, temporary_list, sub):
		self.type = type
		self.size = size
		self.sec_div10 = sec_div10
		self.sub = sub
		self.time_to_atack = -1

			# move
		max_speed, accel, decel, self.lifes = self.movem_attributes(type)
		# Movement(x, y, max_speed, acceleration, decelerate)
		Movement.__init__(self,
							x,
							y,
							max_speed,
							accel,
							decel)
			# fade
		#Fade(color, time_fade, start_fadein)
		Fade.__init__(self,
						color,
						time_fade,
						False)
			# atack
		atack_time, self.reaction, range, fadeout_time_atack = self.atack_attributes(type)
		#Atack(x, y, atack_time, range, color, fadeout_time, sec_div10, temporary_list, enemy_list)
		Atack.__init__(self,
						x,
						y,
						atack_time,
						range,
						color,
						fadeout_time_atack,
						sec_div10,
						temporary_list,
						[sub])


	def take_damage(self):
		self.lifes -= 1
	def is_alive(self):
		return self.lifes > 0

	# max_speed, accel, decel, life
	def movem_attributes(self, type):
		if  type == 0:	#boss
			self.size = self.size*4
			return (1, 0.105, 0.955, 3)
		elif type == 1:	# fast and little
			self.size = self.size*3/4
			return (2, 0.12, 0.98, 1)
		elif type == 2:	# normal
			return (1.8, 0.105, 0.955, 1)
		else:# type 3	# slow and big
			self.size = self.size*2
			return (1, 0.105, 0.955, 1)

	# atack_time, reaction, range, fadeout_time_atack
	def atack_attributes(self, type):
		if  type == 0:	#boss
			return (4, 25, self.size*1.5, 35)
		elif type == 1:	# fast and little
			return (2, 0,self.size*1.5, 25)
		elif type == 2:	# normal
			return (5, 5,self.size*2.5, 40)
		else:# type 3	# slow and big
			return (6, 20,self.size*2.5, 45)

	def in_range(self):
		dist = (self.x - self.sub.x)**2 + (self.y - self.sub.y)**2
		dist = dist**(1/2)
		if dist <= self.range:
			return True

	def calc_direction(self):
		x_speed = 1 if (self.sub.x - self.x) > 0 else -1
		y_speed = 1 if (self.sub.y - self.y) > 0 else -1
		return (x_speed, y_speed)

	def update(self):
			# atack

		if self.time_to_atack == -1 and self.in_range() and self.atack_is_ready():	# ready to atack
			self.time_to_atack = self.reaction			# time to atack
		elif self.time_to_atack > 0:					# wait to atack
			self.time_to_atack -= 1
		elif self.time_to_atack == 0:					# atack
			Atack.atack(self)
			Fade.fadein(self)
			self.time_to_atack -= 1						# goes back to ready

			# movement
		x_speed, y_speed = self.calc_direction()
		Movement.accelerate(self, x_speed, y_speed)
		Movement.update(self)
			# fade
		Fade.update(self)

	def render(self, window):
		x = self.x - self.size/2
		y = self.y - self.size/2
		pygame.draw.rect(window, self.color, (x, y, self.size, self.size))
