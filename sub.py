import pygame
from movement import Movement
from fade import Fade
from atack import Atack

class Sub(Movement, Fade, Atack):
	def __init__(self, x, y, color, size, lifes, atack_time, sec_div10, temporary_list, enemy_list):
		self.size = size
		self.type = -1				# just to atack function work
		self.sec_div10 = sec_div10
		self.lifes = lifes
		self.msgs_list = []			# damage and kill text displays
		# statistics
		self.type_list = []			# types of dead enemies
		self.kills = 0
		self.bombs = 0
		# self.temporary_list = temporary_list
		# self.enemy_list = enemy_list
		# Movement(x, y, max_speed, acceleration, decelerate)
		Movement.__init__(self,
							x,
							y,
							1.8,
							0.105,
							0.955)
		#Fade(color, time_fade, start_fadein)
		Fade.__init__(self,
						color,
						0,
						True)
		#Atack(x, y, atack_time, range, color, fadeout_time, sec_div10, temporary_list, enemy_list)
		Atack.__init__(self,
						x,
						y,
						atack_time,
						size*5,
						color,
						40,
						sec_div10,
						temporary_list,
						enemy_list)

	def take_damage(self):
		self.lifes -= 1
	def is_alive(self):
		return self.lifes > 0

	def generate_points(self, difficulty, start_lifes):
		points = 0
		points += self.sec_div10[0]//5		# add 2 point per second
		points += self.kills * 5			# add 5 per kill
		points -= self.bombs * 5			# rem 5 per bomb used
		for type in self.type_list:			# types of dead enemies
			if type == 0: type = 10			# 10 per boss
			points += type					# add type as points
		points += difficulty*200			# add 100 for final difficulty
		points -= start_lifes*50			# rem 50 per life lost
		return points

	def atack(self):
		if self.atack_is_ready():			# atack is ready
			n_kills, type_list, msgs_list = Atack.atack(self)
			self.type_list += type_list
			self.msgs_list += msgs_list
			self.bombs += 1					# add one use of bomb
			self.kills += n_kills 			# add n kills
			self.atack_boost(n_kills)	# receive bomb recharge boost

	def update(self):
		Movement.update(self)
		Fade.update(self)

	def render(self, window):
		# sub
		x = self.x - self.size/2
		y = self.y - self.size/2
		pygame.draw.rect(window, self.color, (x, y, self.size, self.size))
		# msgs
		for _ in range(len(self.msgs_list)):
			msg = self.msgs_list.pop(0)
			window.blit(msg[1], msg[2])
			if msg[0] > 0:
				self.msgs_list.append((msg[0]-1, msg[1], msg[2]))
