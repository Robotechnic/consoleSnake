import os
import termios
import sys, tty
import shutil
from colorama import Fore, Back
from threading import Thread


class Display:
	def __init__(self):
		size = shutil.get_terminal_size()

		self.width = size[0]
		self.height = size[1]-1

		self.buff = list()

		self.colorEquivBack = {
			"red": Back.RED,
			"blue": Back.BLUE,
			"cyan": Back.CYAN,
			"yellow": Back.YELLOW,
			"white": Back.WHITE,
			"black": Back.BLACK,
			"magenta": Back.MAGENTA,
			"green": Back.GREEN,
			"grey": Back.LIGHTBLACK_EX,
			"lightblue": Back.LIGHTBLUE_EX,
			"lightgreen": Back.LIGHTGREEN_EX,
			"emerald": Back.LIGHTCYAN_EX,
			"orange": Back.LIGHTYELLOW_EX,
			"coral": Back.LIGHTRED_EX,
			"purple": Back.LIGHTMAGENTA_EX,
		}

		self.colorEquivFore = {
			"red": Fore.RED,
			"blue": Fore.BLUE,
			"cyan": Fore.CYAN,
			"yellow": Fore.YELLOW,
			"white": Fore.WHITE,
			"black": Fore.BLACK,
			"magenta": Fore.MAGENTA,
			"green": Fore.GREEN,
			"grey": Fore.LIGHTBLACK_EX,
			"lightblue": Fore.LIGHTBLUE_EX,
			"lightgreen": Fore.LIGHTGREEN_EX,
			"emerald": Fore.LIGHTCYAN_EX,
			"orange": Fore.LIGHTYELLOW_EX,
			"coral": Fore.LIGHTRED_EX,
			"purple": Fore.LIGHTMAGENTA_EX,
		}

		self.backgroundColor = Back.BLACK
		self.textColor = Fore.WHITE

		for y in range(self.height):
			line = list()
			for x in range(self.width):
				line.append([Back.RESET, Fore.RESET, " "])
			self.buff.append(line)

		self.quit = False

	def drawBuffer(self):
		string = ""
		os.system("clear")
		for y in range(self.height):
			for x in range(self.width):
				for c in self.buff[y][x]:
					string += c

		print(string)

	def clear(self):
		for y in range(self.height):
			for x in range(self.width):
				self.buff[y][x] = [Back.RESET, Fore.RESET, " "]

		os.system("clear")

	def background(self, color):
		self.backgroundColor = self.colorEquivBack[color]

	def color(self, color):
		self.textColor = self.colorEquivFore[color]

	def setPixel(self, x, y, char=" "):
		x = int(x)
		y = int(y)
		if x < self.width and y < self.height and x >= 0 and y >= 0:
			self.buff[y][x] = [self.backgroundColor, self.textColor, char[0]]

	def drawString(self, x, y, text):
		lines = text.split("\n")
		for yl in range(len(lines)):
			for xl in range(len(lines[yl])):
					self.setPixel(x+xl , y+yl, lines[yl][xl])


	def centerString(self, y, text):
		lines = text.split("\n")
		for yl in range(len(lines)):
			for xl in range(len(lines[yl])):
					self.setPixel(int(self.width / 2 - len(lines[yl]) / 2)+xl , y+yl, lines[yl][xl])

	def getch(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

		return ch

	def keyPress(self, keyPressed):
		while not self.quit:
			key = self.getch()
			if key == "c":
				self.quit = True
			else:
				keyPressed(key)

	def stop(self):
		self.quit = True

	def run(self, setup, draw, keyPressed=lambda x: print(x)):
		setup()
		self.draw = draw
		t = Thread(target=self.keyPress, args=(keyPressed,))
		t.start()
		while not self.quit:
			# pass
			self.draw()
