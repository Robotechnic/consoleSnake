import shutil
from threading import Thread

import os
if os.name == "nt":
	import msvcrt
else:
	import termios
	import sys, tty

class Display:
	def __init__(self):
		size = shutil.get_terminal_size()

		self.width = size[0]
		self.height = size[1]-1

		self.buff = list()
		self.isDrawedOnce = False

		self.colorEquivBack = {
			"red": "\033[41m",
			"blue": "\033[44m",
			"cyan": "\033[46m",
			"yellow": "\033[103m",
			"white": "\033[47m",
			"black": "\033[40m",
			"magenta": "\033[45m",
			"green": "\033[42m",
			"grey": "\033[100m",
			"lightblue": "\033[104m",
			"lightgreen": "\033[102m",
			"lightcyan": "\033[106m",
			"orange": "\033[43m",
			"pink": "\033[101m",
			"reset": "\033[49m"
		}

		self.colorEquivFore = {
			"red": "\033[31m",
			"blue": "\033[34m",
			"cyan": "\033[36m",
			"yellow": "\033[93m",
			"white": "\033[37m",
			"black": "\033[30m",
			"magenta": "\033[35m",
			"green": "\033[32m",
			"grey": "\033[90m",
			"lightblue": "\033[94m",
			"lightgreen": "\033[92m",
			"lightcyan": "\033[96m",
			"orange": "\033[33m",
			"pink": "\033[91m",
			"reset": "\033[39m"
		}

		self.backgroundColor = self.colorEquivBack["black"]
		self.textColor = self.colorEquivFore["white"]

		for y in range(self.height):
			line = list()
			for x in range(self.width):
				line.append([self.colorEquivBack["reset"], self.colorEquivFore["reset"], " "])
			self.buff.append(line)

		self.quit = False

		if os.name == "nt":
			self.enableWindowsColors()

	def enableWindowsColors(self):
		import ctypes
		STD_OUTPUT_HANDLE = -11
		handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
		mode = ctypes.c_ulong()
		ok = ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode))
		if not ok:
			print("Please, run this programm in a cmd instance")
			self.exit()
			return
		
		ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
		ok = ctypes.windll.kernel32.SetConsoleMode(handle, ctypes.c_ulong(mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING))
		if not ok:
			print("Your current shell isn't compatible with colors.")
			self.exit()
			return

	def clearConsole(self):
		if len(self.buff) == 0 or not self.isDrawedOnce : return
		print("\033[A" * (self.height), end="\r")

	def drawBuffer(self):
		string = ""
		self.clearConsole()
		for y in range(self.height):
			for x in range(self.width):
				for c in self.buff[y][x]:
					string += c

		print(string)

	def clear(self):
		for y in range(self.height):
			for x in range(self.width):
				self.buff[y][x] = [self.colorEquivBack["reset"], self.colorEquivFore["reset"], " "]

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

	

	def keyPress(self, keyPressed):
		if os.name == "nt":
			while not self.quit:
				if msvcrt.kbhit():
					keyPressed(msvcrt.getch().decode("utf-8"))
		else:
			import tty, termios
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			tty.setcbreak(sys.stdin.fileno())
			try:
				while not self.quit:
					keyPressed(sys.stdin.read(1))
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	def exit(self):
		self.quit = True
		self.clearConsole()

	def run(self, setup, draw, keyPressed=lambda _: None):
		setup()
		self.draw = draw
		t = Thread(target=self.keyPress, args=(keyPressed,))
		t.start()
		while not self.quit and t.is_alive():
			self.draw()
			self.drawBuffer()
			self.isDrawedOnce = True
		self.clear()
		self.clearConsole()