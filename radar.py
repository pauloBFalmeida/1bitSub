import pygame
# from math import cos, sin, radians
import math
from fade import Fade

class Radar:
	def __init__(self, sub, range, add_angle, dot_list, enemy_list):
		self.sub = sub
		self.range = range
		self.add_angle = add_angle
		self.angle = 0
		self.dot_list = dot_list
		self.enemy_list = enemy_list

	def update(self):
		render_list = self.dot_list + self.enemy_list
		startAngle = self.angle
		endAngle   = self.angle + self.add_angle
		for obj in render_list:
			x = obj.x - self.sub.x
			y = obj.y - self.sub.y
			# is inside 2D cone
			angle = math.atan2(y,x)*180/ math.pi
			angle += 180
			me = 5 #margin of error
			if (angle+me >= startAngle and angle-me <= endAngle):
				if (x**2 + y**2)**(1/2) < self.range:	# distance
					obj.fadein()
		#
		self.angle = endAngle % 360


class Dot(Fade):
	def __init__(self, x, y, color, size, time_fade, start_fadein):
		self.x = x
		self.y = y
		self.size = size
		Fade.__init__(self, color, time_fade, start_fadein)

	def render(self, window):
		pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.size))
