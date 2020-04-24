import pygame
# from math import cos, sin, radians
import math
from fade import Fade

class Radar:
	def __init__(self, x_center, y_center, add_angle, render_list):
		self.x_center = x_center
		self.y_center = y_center
		self.add_angle = add_angle
		self.angle = 0
		self.render_list = render_list

	def update(self):
		startAngle = self.angle
		endAngle   = self.angle + self.add_angle
		for obj in self.render_list:
			x = obj.x - self.x_center
			y = obj.y - self.y_center
			# is inside 2D cone
			angle = math.atan2(y,x)*180/ math.pi
			angle += 180
			if (angle >= startAngle and angle <= endAngle):
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
		pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.size)
