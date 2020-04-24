class Fade:
	def __init__(self, color, time_fade):
		self.orignal_color = color
		# self.color = (0,0,0)
		self.color = color
		if time_fade == 0:
			self.fadeout = (0,0,0)
		else:
			self.fadeout = (color[0]/time_fade, color[1]/time_fade, color[2]/time_fade)

	def fadein(self):
		self.color = self.orignal_color

	def update(self):
		r = self.color[0] - self.fadeout[0]
		g = self.color[1] - self.fadeout[1]
		b = self.color[2] - self.fadeout[2]
		if r < 1: r = 0
		if g < 1: g = 0
		if b < 1: b = 0
		self.color = (r,g,b)
