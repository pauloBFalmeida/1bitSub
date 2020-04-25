class Movement:
	def __init__(self, x, y, max_speed, acceleration, decelerate):
		self.x = x
		self.y = y		
		self.x_speed = 0
		self.y_speed = 0

		self.max_speed = max_speed
		self.acceleration = acceleration
		self.decelerate = decelerate

	def accelerate(self, x_speed, y_speed):
		# vertex x
		if abs(self.x_speed) < self.max_speed:
			self.x_speed += x_speed * self.acceleration
		# vertex y
		if abs(self.y_speed) < self.max_speed:
			self.y_speed += y_speed * self.acceleration

	def update(self):
		# update position
		self.x += self.x_speed
		self.y += self.y_speed
		# decelerate
		self.x_speed *= self.decelerate
		self.y_speed *= self.decelerate
		# stop infinit deceleration
		if abs(self.x_speed) < 0.1: self.x_speed = 0
		if abs(self.y_speed) < 0.1: self.y_speed = 0
