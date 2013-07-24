#! usr/bin/python
# PongClone- A Python and Pygame version of the classic arcade game.
 #   Copyright (C) 2011 T. S. Hayden Dennison
#
 #   This program is free software: you can redistribute it and/or modify
  #  it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
 #   This program is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.
#
 #   You should have received a copy of the GNU General Public License
  #  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# UPDATE 01/08/2011: added two player mode, updated menu
# UPDATE 01/09/2011: updated ball physics, fixed second player and enemy having unfair adventage by being closer to the wall
# ball is now smaller, with randomized speeds when someone scores.
# UPDATE 01/11/2011: added code to stop ball from resetting its speed to 0
# UPDATE 01/19/2011: added sound effects and better menu.
import pygame, sys, time, random, os, wx, serial, string, ctypes, ctypes.util
from pygame.locals import *
from math import pi

whereislib = ctypes.util.find_library('c')
clib = ctypes.cdll.LoadLibrary(whereislib)

pygame.init()
#size = width, height = 640, 480
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EMG DEMO')
white = [255, 255, 255]
black = [0, 0, 0]
linecolor = 255, 255, 255
linecolor2 = 255, 0 , 0
GREY = 120, 120, 120
RED = 215, 0 , 0
ORANGE = 252, 159, 0
clock = pygame.time.Clock()
ser = serial.Serial(3, 115200, timeout=2)
ser.write("r")
s = ser.readline(9)

###################################################################################################################################################################
# This is a menu class module. You can make text-based menus of any length with it
# SimMen - menu class module with example
 #   Copyright (C) 2011 T. S. Hayden Dennison
#
 #   This program is free software: you can redistribute it and/or modify
  #  it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
 #   This program is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.
#
 #   You should have received a copy of the GNU General Public License
  #  along with this program.  If not, see <http://www.gnu.org/licenses/>
# UPDATE 01/14/2011: fixed window being too big.
# UPDATE 01/15/2011: added mouse control, rewrote most of the menu.update() code.
# UPDATE 01/18/2011: Fixed some syntax and run-time bugs.
# Menu.run() needs the latest event to stop it interfering with your program's event que. You DON'T have to paint over the menu, it takes care of that itself.
# Spent more time (once again) fixing that elusive "maxsize" glitch.

class Menu():
	# Menu class definition
	# need a position to init, minimum
	# Provides some limited cusomizability
	# Uses system font so it's compatible with anything
	def __init__(self, pos, data=[], textsize=32,\
			wordcolor=[255, 255, 0], backcolor=[243, 243, 243], selectedcolor=[0, 255, 255], lprn=20):
		import pygame
		self.rect = pygame.Rect((pos), (0, 0))
		self.data = data
		self.textrects = []
		self.textsurfs = []
		self.cursorpos = 0
		self.pos = pos
		self.font = pygame.font.SysFont(None, 32)
		self.wordcolor = wordcolor
		self.backcolor = backcolor
		self.selectedcolor = selectedcolor
		self.textsize = textsize
		self.looprun = lprn#looprun
		self.scroll = False
		self.selected = False
		for word in self.data:
			self.textsurfs.append(self.font.render(str(word), True, self.wordcolor))
			rect = self.font.render(str(word), True, self.wordcolor).get_rect()
			self.textrects.append(rect)
	def add(self, words):
		# add one or more elements of data
		self.data.extend(words)
		for word in words:
			self.textrects.append(self.font.render(str(word), True, self.wordcolor).get_rect())
			self.textsurfs.append(self.font.render(str(word), True, self.wordcolor))
	def remove(self, item=False):
		if not item:
			# Remove the last element of data
			self.data.pop()
			self.textrects.pop()
			self.textsurfs.pop()
		else:
			thingpop = self.data.index(item)
			self.data.pop(thingpop)
			self.textrects.pop(thingpop)
			self.textsurfs.pop(thingpop)
	def update(self, screen, event):
		import pygame
		# Blit and updated the text box, check key presses
		height = 0
		curpos = []# Stop python from making curpos and self.pos point to the same list
		for n in self.pos:
			curpos.append(n)
		curpos[0] += 1
		self.rect.height = len(self.data)*self.textsize# Define the max height of the text box
		if self.rect.height > screen.get_height():
			self.scroll = True
		else:
			self.scroll = False
		# Define the max width of the text box based on the word length it holds
		maxsize = sorted(self.data)
		maxsize = len(maxsize[0])
		self.rect.width = maxsize*self.textsize/2
		pygame.draw.rect(screen, self.backcolor, self.rect)# Draw the text box
		pygame.draw.rect(screen, self.backcolor, self.rect, 1)# Draw the text box outline
		
		# Update rects and surfaces
		for surf in self.textsurfs:
			if not self.textsurfs.index(surf) == self.cursorpos:
				screen.blit(surf, curpos)
				self.textrects[self.textsurfs.index(surf)].topleft = curpos
			else:
				rect = self.textrects[self.textsurfs.index(surf)]
				rect.topleft = curpos
				surf = self.font.render(str(self.data[self.textsurfs.index(surf)]), True, self.selectedcolor)
				screen.blit(surf, curpos)
			curpos[1] += self.textsize
		e = event
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_UP:
				if self.cursorpos > 0:
					self.cursorpos -= 1
			elif e.key == pygame.K_DOWN:
				if self.cursorpos < len(self.data)-1:
					self.cursorpos += 1
			elif e.key == pygame.K_SPACE:
				self.selected = self.data[self.cursorpos]
		elif e.type == pygame.MOUSEMOTION:
			mousepos = pygame.mouse.get_pos()
			for rect in self.textrects:
				if rect.collidepoint(mousepos):
					self.cursorpos = self.textrects.index(rect)
		elif e.type == pygame.MOUSEBUTTONDOWN:
			self.selected = self.data[self.cursorpos]
		elif e.type == pygame.QUIT:
			self.selected = pygame.QUIT
		return
################################################################################################################################################################
class dummysound():
	def play(self):
		pass

try:
	phase = pygame.mixer.Sound('cool_phase.ogg')
except pygame.error:
	phase = dummysound()
	print 'Error: can\'t load phase.ogg'
try:
	spap = pygame.mixer.Sound('spap.ogg')
except pygame.error:
	spap = dummysound()
	print 'Error: can\'t load spap.ogg'
try:
	die = pygame.mixer.Sound('die.ogg')
except:
	die = dummysound()
	print 'Error: can\'t load die.ogg'

def menu():
	global screen, black, white, clock, Menu
	design = pygame.image.load("design.png")
	#logo = pygame.image.load("ti_logo.jpg")
	titlemenu = Menu([540, 360], wordcolor=[0, 0, 0], selectedcolor=[186, 0, 0], data=['Light Simulation', 'Muscle Race', 'Voltage Challenge','Pong','Quit'])
	screen.fill([243, 243, 243])
	screen.blit(design, (20,165))
	#screen.blit(logo, (0,0))
	font = pygame.font.Font(None, 32)
	screen.blit(font.render('Muscle Sensor PCB - Simulation Demo', True, black, [243, 243, 243]), [450, 100])
	pygame.display.flip()
	while not titlemenu.selected:
		titlemenu.update(screen, pygame.event.poll())
		clock.tick(30)
		pygame.display.flip()
	if titlemenu.selected == 'Light Simulation':
         light()
		#newGame()
	elif titlemenu.selected == 'Muscle Race':
		musclerace()
	elif titlemenu.selected == 'Voltage Challenge':
		volts()
	elif titlemenu.selected == 'Pong':
		newGame(True)
	else:
		pygame.quit()
		sys.exit()

def light():
	global white, black, screen, ser
	
	values = 119
	values2 = 452
	tups = [(0,0)]*400
	backup = [452]*400

	for count in range(0,400):
		values+=1
		#values2+=2
		tups[count] = (values, values2)
	
	#screen.fill(black)
	font = pygame.font.Font(None, 32)

	lighton = pygame.image.load("on.jpg").convert()
	#on_rect = lighton.get_rect()
	lighton.set_alpha(100)
	lightoff = pygame.image.load("off.png").convert()
	#off_rect = lightoff.get_rect()
	lightoff.set_alpha(100)
	s = 1
	while True:
		screen.fill(black)
		screen.blit(font.render('Turn the Light On & Off', True, white, black), [390, 20])
		screen.blit(lighton, (650,0))
		screen.blit(lightoff, (697,30))
		#if i > 0:
		#	i-=1
		#	lightoff.set_alpha(i)
		#else:
		#	i = 100
		
		#adjusted on 1024 scale
		#print s

		#print s
		#take serial input	
		ser.write("r")
		s = ser.readline(9)
		spst = string.split(str(s),';')

		
		#Graph
		del tups[0]
		#print spst[1]
		s = -1*(clib.atoi(spst[1]) *0.05)+450
		print spst[1]
		lightoff.set_alpha(100-(clib.atoi(spst[1])-337)/13)
		
		#print s
		backup[399] = s
		values = 119
		for count2 in range(0,399):
			values+=1
			tups[count2] = (values, backup[count2])
		values+=1
		del backup[0]
		backup.insert(399, 0)
		tups.insert(399, (values, s))
		
		pygame.draw.lines(screen, linecolor2, False, tups, 2)
		pygame.draw.rect(screen, linecolor, pygame.Rect((120,200),(400,256)), 3)
		
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					menu()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		clock.tick(30)

def musclerace():
	global white, black, ser, screen, GREY
	ship1_x = 0
	ship2_x = 0
	ship1 = pygame.image.load("ship_1.png")
	ship2 = pygame.image.load("ship_2.png")
	ship1_off = pygame.image.load("ship_1_off.png")
	ship2_off = pygame.image.load("ship_2_off.png")		
	launch = pygame.image.load("launchpad.png")
	paddlescore = pygame.font.Font(None, 32)
	screen.fill(black)
	screen.blit(paddlescore.render('3', True, white), (640,360))
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('2', True, white), (640,360))
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('1', True, white), (640,360))
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('GO!', True, white), (640,360))
	pygame.display.flip()
 
	while 1:
		clock.tick(50)
 
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					menu()
			if event.type == pygame.QUIT:
				sys.exit()
 
		screen.fill(black)
	
		#serial input
		ser.write("r")
		s = ser.readline(9)
		spst = string.split(str(s),';')
		
		#win at 950
		#ship1_x = 500#int(s)
		#ship2_x = ship1_x
		print spst[0], spst[1]
		#print ship1_x, ship2_x


		pygame.draw.line(screen, white, (1200, 0), (1200,720), 2)
		if ship1_x < 3:
			screen.blit(ship1_off, (ship1_x,165))
		else:
			screen.blit(ship1, (ship1_x, 165))
	
		if ship2_x < 3:
			screen.blit(ship2_off, (ship2_x,400))
		else:
			screen.blit(ship2, (ship2_x, 400))
		
		#speed
		speed1 = clib.atoi(spst[0]) * 0.0005
		if speed1 < 1:
			speed1 = 0
		ship1_x = ship1_x + speed1
		
		speed2 = clib.atoi(spst[1]) * 0.0005
		if speed2 < 1:
			speed2 = 0
		ship2_x = ship2_x + speed2
		
		pygame.draw.rect(screen, GREY, (0, 0, 134, 720))
		screen.blit(launch, (12,0))
		
		#win case
		if ship1_x > 950 or ship2_x > 950:
			if ship1_x > ship2_x:
				#screen.fill(black)
				screen.blit(paddlescore.render('Blue wins!', True, white), (640,360))
				pygame.display.flip()
			else:
				screen.blit(paddlescore.render('Green wins!', True, white), (640,360))
				pygame.display.flip()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							menu()
		

		#pygame.draw.rect(screen, GREY, (0, 430, 20, 70))
		pygame.display.flip()
	
def volts():
	global white, black, GREY, ser, screen
	arrow = pygame.image.load("arrow.png").convert_alpha()
	arrow2 = pygame.image.load("arrow.png").convert_alpha()
	font = pygame.font.Font(None, 32)
	timer = 0
	highest_value = 0
	paddlescore = pygame.font.Font(None, 32)
	screen.fill(black)
	screen.blit(paddlescore.render('3', True, white), (640,360))
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('2', True, white), (640,360))
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('1', True, white), (640,360))
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('GO!', True, white), (640,360))
	pygame.display.flip()
	
	while 1:
		clock.tick(50)
		timer = timer + 1
 
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					menu()
			if event.type == pygame.QUIT:
				sys.exit()
 
		screen.fill(black)
		screen.blit(font.render('Muscle Voltage Challenge', True, white, black), [488, 20])

		#ship2 = pygame.image.load("ship_2.png")
		#ship1_off = pygame.image.load("ship_1_off.png")
		#ship2_off = pygame.image.load("ship_2_off.png")
		#launch = pygame.image.load("launchpad.png")
  
		ser.write("r")
		s = ser.readline(9)
		spst = string.split(str(s),';')
		#put in a timer before start

  
 
		#draw left gauge
		pygame.draw.circle(screen, GREY, (320, 360), 250)
		#pygame.draw.circle(screen, GREY, (960, 360), 250)
		pygame.draw.circle(screen, white, (320, 360), 235)
		#pygame.draw.circle(screen, WHITE, (960, 360), 235)
		pygame.draw.arc(screen, GREY,[170,202,310,310], 0, pi+0.05, 4)
		pygame.draw.arc(screen, ORANGE,[170,202,310,310], pi/4.1, pi/2.2, 5)
		pygame.draw.arc(screen, RED,[170,202,310,310], 0, pi/4, 6)
		pygame.draw.line(screen, black, (85, 360), (555,360), 3)
  
		#draw right gauge
		pygame.draw.circle(screen, GREY, (960, 360), 250)
		#pygame.draw.circle(screen, GREY, (320, 360), 250)
		pygame.draw.circle(screen, white, (960, 360), 235)
		#pygame.draw.circle(screen, WHITE, (320, 360), 235)
		pygame.draw.arc(screen, GREY,[810,202,310,310], 0, pi+0.05, 4)
		pygame.draw.arc(screen, ORANGE,[810,202,310,310], pi/4.1, pi/2.2, 5)
		pygame.draw.arc(screen, RED,[810,202,310,310], 0, pi/4, 6)
		pygame.draw.line(screen, black, (1195, 360), (725,360), 3)
		
		# (a,b) (c, d)
		# (300,5000) (88,-88) #3796
		# ((x -a)*(d-c))/(b-a) + C
		print spst[0], spst[1]
		angle = ((clib.atoi(spst[0])-300) * -0.0375) + 88
		angle2 = ((clib.atoi(spst[1])-500) * -0.0375) + 88
		if angle > 88:
			angle = 88
		if angle2 > 88:
			angle2 = 88
		#print angle, angle2
		rotarrow = rot_center(arrow, angle)
		rotarrow2 = rot_center(arrow2, angle2)
		#pygame.draw.rect(screen, GREY, (0, 0, 134, 720))
		screen.blit(rotarrow, (128,162))
		screen.blit(rotarrow2, (758,162))
		#left box
		pygame.draw.rect(screen, black, (236, 416, 168, 78))
		pygame.draw.rect(screen, GREY, (240, 420, 160, 70))
		#right box
		pygame.draw.rect(screen, black, (1044, 416, -168, 78))
		pygame.draw.rect(screen, GREY, (1040, 420, -160, 70))
		
		if angle>88:
			p1output = 0
		else:
			p1output = clib.atoi(spst[0])
			
		if angle2>88:
			p2output = 0
		else:
			p2output = clib.atoi(spst[1])-200
			
		screen.blit(font.render(str(p1output), True, white, GREY), [295, 445])
		screen.blit(font.render(str(p2output), True, white, GREY), [930, 445])
		
		ang = spst[0]
		ang2 = spst[1]
		
		if timer > 200:
			if ang > ang2:
				if ang > highest_value:
					highest_value = ang
					left_winner = 1
			else:
				if ang2 > highest_value:
					highest_value = ang2
					left_winner = 0
		
		if timer > 1100:
			if left_winner:
				screen.blit(font.render('Left wins!', True, white), (585,360))
				screen.blit(font.render(str(highest_value), True, white), (585,388))
				pygame.display.flip()
			else:
				screen.blit(font.render('Right wins!', True, white), (585,360))
				screen.blit(font.render(str(highest_value), True, white), (585,388))
				pygame.display.flip()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							menu()
 
		pygame.display.flip()


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
def newGame(twoplayer=False):
	global white, black
	class Paddle():
		def __init__(self, upkey, downkey):
			global screen
			self.area = [screen.get_width(), screen.get_height()]
			self.pos = [20, self.area[1]/2]
			self.rect = Rect((self.pos), (10, 140))
			self.speed = 5
			self.score = 0
			self.upkey, self.downkey = upkey, downkey
		def update(self, position):
			global screen, white
			position = position + 500
			self.rect = Rect((10,position),(10,140))
			#keys = pygame.key.get_pressed()
			#if keys[self.upkey]:
			#	if self.rect.top > 20:
			#		self.rect.top -= self.speed
			#elif keys[self.downkey]:
			#	if self.rect.bottom < self.area[1]-20:
			#		self.rect.bottom += self.speed
			pygame.draw.rect(screen, white, self.rect)
			return
	class Paddle2():
		def __init__(self, upkey, downkey):
			global screen
			self.area = [screen.get_width(), screen.get_height()]
			self.pos = [20, self.area[1]/2]
			self.rect = Rect((self.pos), (10, 140))
			self.speed = 5
			self.score = 0
			self.upkey, self.downkey = upkey, downkey
		def update(self, position):
			global screen, white
			position = position + 520
			self.rect = Rect((1270,position),(10,140))
			#keys = pygame.key.get_pressed()
			#if keys[self.upkey]:
			#	if self.rect.top > 20:
			#		self.rect.top -= self.speed
			#elif keys[self.downkey]:
			#	if self.rect.bottom < self.area[1]-20:
			#		self.rect.bottom += self.speed
			pygame.draw.rect(screen, white, self.rect)
			return
	
	class Enemy():
		def __init__(self):
			global screen
			self.area = [screen.get_width(), screen.get_height()]
			self.pos = [self.area[0]-30, self.area[1]/2]
			self.rect = Rect((self.pos), (10, 40))
			self.speed = 5
			self.score = 0
		def update(self, ball):
			global screen, white
			if ball.rect.centery < self.rect.centery:
				if self.rect.top > 20:
					self.rect.centery -= self.speed
			if ball.rect.centery > self.rect.centery:
				if self.rect.bottom < self.area[1]-20:
					self.rect.centery += self.speed
			pygame.draw.rect(screen, white, self.rect)
			return

	class Ball():
		def __init__(self):
			global screen
			self.pos = [screen.get_width()/2, screen.get_height()/2]
			self.center = self.pos
			self.rect = Rect((self.pos), (15, 15))
			self.speed = [random.randint(-3, 3), random.randint(-3, 3)]
			while self.speed[0] == 0:
				self.speed[0] = random.randint(-3, 3)
			while self.speed[1] == 0:
				self.speed[1] = random.randint(-3, 3)
			self.area = [screen.get_width(), screen.get_height()]
			self.paddlecols = 0
		def update(self, paddle, enemy):
			global screen, white, phase, spap, die
			if self.rect.top <= 0 or self.rect.bottom >= self.area[1]:
				phase.play()
				self.speed[1] = -self.speed[1]
				if self.speed[1] < 0:
					self.speed[1] -= 1
				elif self.speed[1] > 0:
					self.speed[1] += 1
			if self.rect.right >= self.area[0]:
				die.play()
				paddle.score += 1
				self.rect.center = self.center
				self.speed[0] = 0
				self.speed[1] = 0
				while self.speed[0] == 0:
					self.speed[0] = random.randint(-3, 3)
				while self.speed[1] == 0:
					self.speed[1] = random.randint(-3, 3)
			elif self.rect.left <= 0:
				die.play()
				enemy.score += 1
				self.rect.center = self.center
				self.speed[0] = 0
				self.speed[1] = 0
				while self.speed[0] == 0:
					self.speed[0] = random.randint(-3, 3)
				while self.speed[1] == 0:
					self.speed[1] = random.randint(-3, 3)
			if self.rect.colliderect(paddle.rect) or self.rect.colliderect(enemy.rect):
				self.paddlecols += 1
				if self.paddlecols > 1:
					if self.rect.colliderect(paddle.rect):
						self.rect.right += 10
					elif self.rect.colliderect(enemy.rect):
						self.rect.left -= 10
				else:
					spap.play()
					self.speed[0] = -self.speed[0]
					if self.speed[0] < 0:
						self.speed[0] -= 1
					elif self.speed[0] > 0:
						self.speed[0] += 1
			else:
				self.paddlecols = 0
			if self.speed[0] > 6:
				self.speed[0] = 6
			elif self.speed[0] < -6:
				self.speed[0] = -6
			self.rect = self.rect.move(self.speed)
			pygame.draw.rect(screen, white, self.rect)
			return
	ball = Ball()
	paddle_two = Paddle2(pygame.K_UP, pygame.K_DOWN)
	paddle = Paddle(pygame.K_w, pygame.K_s)
	paddle_two.pos = [screen.get_width()-30, screen.get_height()/2]
	paddle_two.rect.center = paddle_two.pos
	enemy = Enemy()
	gameLoop(paddle, enemy, ball, twoplayer, paddle_two)
	startOver()
def gameLoop(paddle, enemy, ball, twoplayer, paddle_two):
	global screen, white, black, clock, ser
	paddlescore = pygame.font.Font(None, 32)
	enemyscore = pygame.font.Font(None, 32)
	topscore = 0
	screen.fill(black)
	screen.blit(paddlescore.render('3', True, white), ball.center)
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('2', True, white), ball.center)
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('1', True, white), ball.center)
	pygame.display.flip()
	time.sleep(1)
	screen.fill(black)
	screen.blit(paddlescore.render('GO!', True, white), ball.center)
	pygame.display.flip()
	time.sleep(0.5)
	while not topscore > 2:
		screen.fill(black)
		# (a,b) (c, d)
		# ((x -a)*(d-c))/(b-a) + C
		ser.write("r")
		s = ser.readline(9)
		spst = string.split(str(s),';')
		pos1 = ((clib.atoi(spst[0])-300)*0.46)+80
		pos2 = ((clib.atoi(spst[1])-540)*0.46)+80
		print spst[0], spst[1]
		paddle.update(-1*pos1)
		if twoplayer:
			paddle_two.update(-1*pos2)
			ball.update(paddle, paddle_two)
		else:
			enemy.update(ball)
			ball.update(paddle, enemy)
		pygame.draw.line(screen, white, [screen.get_width()/2, 0], [screen.get_width()/2, screen.get_height()])
		if twoplayer:
			scores = [paddle.score, paddle_two.score]
		else:
			scores = [paddle.score, enemy.score]
		topscore = sorted(scores, reverse=True)
		topscore = topscore[0]
		screen.blit(paddlescore.render(str(paddle.score), True, white), [590, 0])
		if twoplayer:
			screen.blit(enemyscore.render(str(paddle_two.score), True, white), [680, 0])
		else:
			screen.blit(enemyscore.render(str(enemy.score), True, white), [680, 0])
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					menu()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		clock.tick(50)
		pygame.display.flip()
	screen.fill(black)
	if not twoplayer:
		if paddle.score == topscore:
			screen.blit(paddlescore.render('You Won! You beat the machine, proving that YOU', True, white, black), [0, 0])
			screen.blit(paddlescore.render('are the Master Pong Player! Well, not really.', True, white, black), [0, 32])
			screen.blit(paddlescore.render('But it was a nice thought. (Press any key to', True, white, black), [0, 64])
			screen.blit(paddlescore.render('return to the menu).', True, white, black), [0, 98])
			pygame.display.flip()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
						 menu()
		else:
			screen.blit(paddlescore.render('You Lost! This bucket of bolts beat a smart human like', True, white, black), [0, 0])
			screen.blit(paddlescore.render('yourself! Too bad! Press any key to return to menu.', True, white, black), [0, 32])
			pygame.display.flip()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						menu()
	else:
		if paddle.score == topscore:
			screen.blit(paddlescore.render('Player 1 won! (left side). Press any key to', True, white, black), [580, 580])
			screen.blit(paddlescore.render('to menu.', True, white, black), [580, 612])
			pygame.display.flip()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						menu()
		else:
			screen.blit(paddlescore.render('Player 2 won! (right side). Press any key to', True, white, black), [580, 580])
			screen.blit(paddlescore.render('to menu.', True, white, black), [580, 612])
			pygame.display.flip()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						menu()

if __name__ == '__main__':
	menu()
