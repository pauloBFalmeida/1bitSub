import pygame
# import sub, enemy
from random import randint
from sub import Sub
from enemy import Enemy
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
		self.game_running = True
		self.display_end_screen = True
		self.FPS = 60
		self.background = (0, 0, 0)
		self.difficulty = 0

		self.time_radar = self.FPS * 4 	# seconds to complete a cicle
		self.range_radar = 250
		self.time_fadeout = 200
		self.n_dots = 25				# this will be squared

		self.atack_time = 5 	# seconds to sub atack
		self.color = (50, 175, 40)	# green
		self.size = 7
		self.lifes = 5

	def add_second(self):
		self.sec_div10[0] += 1
		self.difficulty = int( (self.sec_div10[0]/10)//60 )
		pygame.time.set_timer(pygame.NUMEVENTS-1, 100)		# wait 1/10 sec

	def start(self):
			# start sec_div10 count
		self.sec_div10 = [-1]
		self.add_second()
			# create temporary list
		self.temporary_list = []
			# create enemy list
		self.enemy_list = []
			# create sub
		x_center = self.width//2
		y_center = self.height//2
		# Sub(x,y, color, size, lifes, atack_time, sec_div10, temporary_list, enemy_list)
		self.sub = Sub(
			x_center,
			y_center,
			self.color,
			self.size,
			self.lifes,
			self.atack_time,
			self.sec_div10,
			self.temporary_list,
			self.enemy_list)
			# create radar dots
		qtd = self.n_dots
		width = self.width / qtd
		height = self.height / qtd
		self.dot_list = []
		for i in range(qtd):
			for j in range(qtd):
				# Dot(x, y, color, size, time_fade, start_fadein)
				self.dot_list.append(Dot(
									width*j+width//2,
									height*i+height//2,
									self.color,
									0,
									self.time_fadeout, False))
			# create radar
		# Radar(sub, range, add_angle, dot_list, enemy_list)
		self.radar = Radar(
						self.sub,
						self.range_radar,
						360/self.time_radar,
						self.dot_list,
						self.enemy_list)
			# start enemies spawn countdown
		pygame.time.set_timer(pygame.USEREVENT+1, 5000)		# normal enemies
		pygame.time.set_timer(pygame.USEREVENT+2, 30000)	# boss

	def create_enemy(self):
		# create enemy
		type = randint(1,3)	# type of enemies
		qtd = randint(1,3)	# number of enemies
		for _ in range(qtd):
			# random pos in x axis
			if randint(0,1) == 0:
				x = randint(0,self.width)
				y = 0 if randint(0,1) == 0 else self.height	#
			# random pos in y axis
			else:
				x = 0 if randint(0,1) == 0 else self.width	#
				y = randint(0,self.height)
			# Enemy(x,y, type, color, size, time_fade, sec_div10, temporary_list, sub)
			self.enemy_list.append(Enemy(
									x,
									y,
									type,
									self.color,
									self.size,
									self.time_fadeout,
									self.sec_div10,
									self.temporary_list,
									self.sub))
		# call in another 6 to 9 sec
		time = randint(6,9) - self.difficulty
		if time < 0: time = 0
		pygame.time.set_timer(pygame.USEREVENT+1, time*1000)

	def create_boss(self):
		# create boss
		# random pos in x axis
		if randint(0,1) == 0:
			x = randint(0,self.width)
			y = 0 if randint(0,1) == 0 else self.height	#
		# random pos in y axis
		else:
			x = 0 if randint(0,1) == 0 else self.width	#
			y = randint(0,self.height)
		# Enemy(x,y, type, color, size, time_fade, sec_div10, temporary_list, sub)
		self.enemy_list.append(Enemy(
								x,
								y,
								0,
								self.color,
								self.size,
								self.time_fadeout,
								self.sec_div10,
								self.temporary_list,
								self.sub))
		# call in another 30 to 45 sec
		time = randint(30,45) - self.difficulty*3
		if time < 0: time =0
		pygame.time.set_timer(pygame.USEREVENT+2, time*1000)


	def stats(self, window):
		font = pygame.font.SysFont("calibri", 20)
		porcentage = self.sub.atack_ready_porcent()
		srt_porcentage = "#"*(self.atack_time-porcentage) + "_"*porcentage
		text = "bomb: ["+srt_porcentage+"]"
		text += " lifes:"+str(self.sub.lifes)
		text += " difficulty:"+str(self.difficulty)
		text += " sec:"+str(self.sec_div10[0]/10)
		textbox = font.render(text, True, self.color)
		x = 15
		y = self.height - textbox.get_height() - 15
		window.blit(textbox, (x,y))

	def input(self, keys):
		margin = 15
		# Player Controls
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			if self.sub.x > 0 + margin:
				self.sub.accelerate(-1,0)
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			if self.sub.x < self.width - margin:
				self.sub.accelerate(1,0)
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			if self.sub.y > 0 + margin:
				self.sub.accelerate(0,-1)
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			if self.sub.y < self.height - margin:
				self.sub.accelerate(0,1)
		if keys[pygame.K_SPACE]:
			self.sub.atack()
		if keys[pygame.K_ESCAPE]:
			self.game_running = False

	def logic(self):
		for dot in self.dot_list:			# radar dots
			dot.update()
		self.sub.update()					# player
		for enemy in self.enemy_list:		# enemies
			enemy.update()
		if not self.sub.is_alive():		# player died
			self.game_running = False
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
		for temp in self.temporary_list:	# explosions
			temp[1].render(window)
		for enemy in self.enemy_list:		# enemies
			enemy.render(window)
		self.sub.render(window)				# player
		self.stats(window)					# stats
		pygame.display.update()				# update screen


	def settings(self):
		entry = ""
		while entry != "/quit":
			print("type: /quit to save and leave settings")
			print("/n_dots to change number of dots in radar")
			print("/lifes to change your number of lifes")
			print("/radar_time to change the number of seconds to complete a turn")
			print("/radar_range to change the range to see enemies")
			entry = input()
			if entry == "/n_dots":
				print("current number: "+str(self.n_dots))
				print("enter the number of dots (this number will be squared)")
				self.n_dots = int(input())
			elif entry == "/lifes":
				print("current number: "+str(self.lifes))
				print("enter the number of lifes")
				self.lifes = int(input())
			elif entry == "/radar_time":
				print("current number: "+str(self.time_radar/self.FPS))
				print("enter the number of lifes")
				self.time_radar = self.FPS * int(input())
			elif entry == "/radar_range":
				print("current number: "+str(self.range_radar))
				print("enter the number of lifes")
				self.range_radar = int(input())
		print("settings have been saved, you can go back to the game")


	def wait_to_start(self):
		font = pygame.font.SysFont("calibri", 30)
		text = font.render("Press G to start", True, self.color)
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

		text = font.render("press C to open game settings on terminal", True, self.color)
		x = self.width//2 - text.get_width()//2
		y = self.height*2//3 + text.get_height()//2
		self.win.blit(text, (x,y))

		pygame.display.update()

		while True:							# wait to player press 'g'
			event = pygame.event.wait()
			if event.type == pygame.QUIT:	# kill screen
				self.game_running = False
				self.running = False
				self.display_end_screen = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:	# start game
					break
				if event.key == pygame.K_c:	# start game
					self.settings()


	def end_screen(self):
		font = pygame.font.SysFont("calibri", 30)
		text = font.render("press G to start a new game", True, self.color)
		x = self.width//2 - text.get_width()//2
		y = self.height//4 - text.get_height()//2
		self.win.blit(text, (x,y))

		text = font.render("You died", True, self.color)
		x = self.width//2 - text.get_width()//2
		y = self.height//2 - text.get_height()//2
		self.win.blit(text, (x,y))

		points = self.sub.generate_points(self.difficulty, self.lifes)
		text = font.render("points:"+str(points), True, self.color)
		x = self.width//2 - text.get_width()//2
		y = self.height//2 + text.get_height()//2
		self.win.blit(text, (x,y))

		pygame.display.update()

		while True:							# wait to player press 'g'
			event = pygame.event.wait()
			if event.type == pygame.QUIT:	# kill screen
				self.running = False
				self.game_running = False
				self.display_end_screen = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:	# start game
					self.game_running = True
					break

def main():
	game = Py1bitSub(800, 600, "1bitSub")

	game.wait_to_start()					# wait to player press 'g'
	while game.running:
		game.start()							# start game

		while game.game_running:
			game.clock.tick(game.FPS)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game.game_running = False
					game.running = False
					game.display_end_screen = False
				elif event.type == pygame.NUMEVENTS-1:
					game.add_second()
				elif event.type == pygame.USEREVENT+1:
					game.create_enemy()
				elif event.type == pygame.USEREVENT+2:
					game.create_boss()

			game.input(pygame.key.get_pressed())
			game.logic()
			game.render(game.win)

		if game.display_end_screen: game.end_screen()

if __name__ == "__main__":
	main()
	pygame.quit()
	quit()
