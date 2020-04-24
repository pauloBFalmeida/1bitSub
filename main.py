import pygame
# import sub, enemy
from sub import Sub
from radar import Radar, Dot
pygame.init()

class Py1bitSub:
	def __init__(self, width, height, title):
		self.width = width
		self.height = height
		self.win = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)

		self.clock = pygame.time.Clock()
		self.running = True
		self.FPS = 60
		self.background = (0, 0, 0)

		self.time_radar = 4 # seconds to complete a cicle
		self.time_radar *= self.FPS
		self.time_fadeout = 200

		self.color = (50, 175, 40)	# green
		# self.color = (255, 0, 0)	# test
		self.size = 7

		self.atack_time	= 5 * self.FPS
		self.atack_cooldown = 0

	def start(self):
		# Sub(x, y, color, size, time_fade, range)
		self.sub = Sub(self.width//2, self.height//2, self.color, self.size, 0, 10)
		self.sub.fadein()
		# create enemy list
		# self.enemy_list = []
		self.enemy_list = [Sub(self.width//2, self.height//2, (255,255,255), self.size, 0, 10)]	# test
		# create radar dots
		qtd = 10
		width = self.width / qtd
		height = self.height / qtd
		self.dot_list = []
		for i in range(qtd):
			for j in range(qtd):
				# Dot(x, y, color, size, time_fade)
				self.dot_list.append(Dot(width*j+width//2, height*i+height//2, self.color, 0, self.time_fadeout))
		# Radar(x_center, y_center, add_angle, render_list)
		self.radar = Radar(self.width//2, self.height//2, 360/self.time_radar, self.dot_list+self.enemy_list)
		# create temporary list
		self.temporary_list = []

	def atack(self):
		self.sub.add_bomb()
		if self.atack_cooldown == 0:
			x = self.sub.x
			y = self.sub.y
			size = self.size*5
			for enemy in self.enemy_list:
				dist = (x - enemy.x)**2 + (y - enemy.y)**2
				dist = dist**(1/2)
				# enemy center inside the radius
				if dist-self.size/2 <= size:
					self.enemy_list.remove(enemy)
					self.sub.add_elimination()
			# animation
			self.temporary_list.append( (40,Dot(x+self.size, y+self.size, self.color, size, 40)) )
			self.atack_cooldown = self.atack_time

	def stats(self, window):
		font = pygame.font.SysFont("calibri", 20)
		porcentage = int(self.atack_cooldown / self.atack_time * 10)
		srt_porcentage = "#"*(9-porcentage) + "_"*porcentage
		text = "bomb: ["+srt_porcentage+"]"+" sec:"+str(self.sub.sec)
		textbox = font.render(text, True, self.color)
		x = 15
		y = self.height - textbox.get_height() - 15
		window.blit(textbox, (x,y))

	def input(self, keys):
		# Player Controls
		if keys[pygame.K_a]:
			if self.sub.x > 0:
				self.sub.accelerate(-1,0)
		if keys[pygame.K_d]:
			if self.sub.x < self.width:
				self.sub.accelerate(1,0)
		if keys[pygame.K_w]:
			if self.sub.y > 0:
				self.sub.accelerate(0,-1)
		if keys[pygame.K_s]:
			if self.sub.y < self.height:
				self.sub.accelerate(0,1)
		if keys[pygame.K_f]:
			self.sub.fadein()
		if keys[pygame.K_SPACE]:
			self.atack()
		if keys[pygame.K_ESCAPE]:
			self.running = False

	def logic(self):
		self.sub.update()					# player
		self.atack_cooldown = 0 if self.atack_cooldown == 0 else self.atack_cooldown - 1
		for dot in self.dot_list:			# radar dots
			dot.update()
		for enemy in self.enemy_list:		# enemies
			enemy.update()
		self.radar.update()					# radar
		for _ in range(len(self.temporary_list)):
			temp = self.temporary_list.pop()
			if temp[0] > 0:
				temp[1].update()
				self.temporary_list.append( (temp[0]-1, temp[1]) )


	def render(self, window):
		window.fill(self.background)		# background
		for dot in self.dot_list:			# radar dots
			dot.render(window)
		for enemy in self.enemy_list:		# enemies
			enemy.render(window)
		for temp in self.temporary_list:
			temp[1].render(window)
			# print('obaa')
		self.sub.render(window)				# player
		self.stats(window)					# stats
		pygame.display.update()				# update screen


	def wait_to_start(self):
		font = pygame.font.SysFont("calibri", 30)
		text = font.render("press G to start", True, self.color)
		x = self.width//2 - text.get_width()//2
		y = self.height//4 - text.get_height()//2
		self.win.blit(text, (x,y))

		text = font.render("use wasd to move", True, self.color)
		x = self.width//2 - text.get_width()//2
		y = self.height//2 - text.get_height()//2
		self.win.blit(text, (x,y))

		text = font.render("space to atack", True, self.color)
		x = self.width//2 - text.get_width()//2
		y = self.height//2 + text.get_height()//2
		self.win.blit(text, (x,y))

		pygame.display.update()

		while True:							# wait to player press 'g'
			event = pygame.event.wait()
			if event.type == pygame.QUIT:	# kill screen
				game.running = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:
					break

def main():
	game = Py1bitSub(800, 600, "1bitSub")
	game.wait_to_start()					# wait to player press 'g'
	game.start()							# start game

	while game.running:
		game.clock.tick(game.FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.running = False

		game.input(pygame.key.get_pressed())
		game.logic()
		game.render(game.win)


if __name__ == "__main__":
	main()
	pygame.quit()
	quit()
