import pygame
from radar import Dot

class Atack:
	def __init__(self, x, y, atack_time, range, color, fadeout_time, sec_div10, temporary_list, enemy_list):
		self.x = x
		self.y = y
		self.atack_time = atack_time*10		# machup with seconds/10
		self.atack_ready = 0
		self.range = range
		self.color = color
		self.fadeout_time = fadeout_time
		self.sec_div10 = sec_div10
		self.temporary_list = temporary_list
		self.enemy_list = enemy_list

	def atack_boost(self, n_kills):
		self.atack_ready -= n_kills * 10

	def atack_ready_porcent(self):
		time = self.atack_ready - self.sec_div10[0]
		return 0 if time < 0 else int(time/10)+1

	def atack_is_ready(self):
		return False if self.sec_div10[0] < self.atack_ready else True

	def atack(self):
		# atack is ready
		n_kills = 0
		type_list = []
		msgs_list = []
		enemies = list(self.enemy_list)
		for enemy in enemies:
			dist = (self.x - enemy.x)**2 + (self.y - enemy.y)**2
			dist = dist**(1/2)
			# enemy center inside the radius
			if dist-enemy.size/2 <= self.range:
				enemy.take_damage()
				if not enemy.is_alive():	# enemy is dead
					self.enemy_list.remove(enemy)
					msgs_list.append(self.print_kill(enemy))
					type_list.append(enemy.type)
					n_kills += 1
				else:						# enemy is alive
					msgs_list.append(self.print_damage(enemy))

	 	# animation
		self.temporary_list.append(
			(self.fadeout_time, Dot(
									self.x,
									self.y,
									self.color,
									self.range,
									self.fadeout_time,
									True)) )
		self.atack_ready = self.sec_div10[0] + self.atack_time
		return (n_kills, type_list, msgs_list)


	def print_msg(self, text, enemy):
		size = int(enemy.size)
		if size < 6: size = 6
		if size > 15: size = 15
		font = pygame.font.SysFont("calibri", size)
		textbox = font.render(text, True, self.color)
		x = int(enemy.x)
		y = int(enemy.y - enemy.size - textbox.get_height())
		return (60, textbox, (x,y))

	def print_damage(self, enemy):
		return self.print_msg("DAMAGE", enemy)

	def print_kill(self, enemy):
		return self.print_msg("KILL", enemy)
