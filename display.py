import os
import shutil
from colorama import Fore, Back

class Display:

	def __init__(self):
		size = shutil.get_terminal_size()
		self.width = size[0]
		self.height  = size[1]

		self.buff = list()

		self.colorEquivBack = {
			"red":Back.RED,
			"blue":Back.BLUE,
			"cyan":Back.CYAN,
			"yellow":Back.YELLOW,
			"white":Back.WHITE,
			"black":Back.BLACK,
			"magenta":Back.MAGENTA,
			"green":Back.GREEN,
			"grey":Back.LIGHTBLACK_EX,
			"lightblue":Back.LIGHTBLUE_EX,
			"lightgreen":Back.LIGHTGREEN_EX,
			"emerald":Back.LIGHTCYAN_EX,
			"orange":Back.LIGHTYELLOW_EX,
			"coral":Back.LIGHTRED_EX,
			"purple":Back.LIGHTMAGENTA_EX
		}

		self.colorEquivFore = {
			"red":Fore.RED,
			"blue":Fore.BLUE,
			"cyan":Fore.CYAN,
			"yellow":Fore.YELLOW,
			"white":Fore.WHITE,
			"black":Fore.BLACK,
			"magenta":Fore.MAGENTA,
			"green":Fore.GREEN,
			"grey":Fore.LIGHTBLACK_EX,
			"lightblue":Fore.LIGHTBLUE_EX,
			"lightgreen":Fore.LIGHTGREEN_EX,
			"emerald":Fore.LIGHTCYAN_EX,
			"orange":Fore.LIGHTYELLOW_EX,
			"coral":Fore.LIGHTRED_EX,
			"purple":Fore.LIGHTMAGENTA_EX
		}

		self.backgroundColor = Back.BLACK
		self.textColor = Fore.WHITE

		for y in range(self.height):
			line = list()
			for x in range(self.width):
				line.append([Back.RESET,Fore.RESET," "])
			self.buff.append(line)

		self.quit = False

	def drawBuffer(self):
		for y in range(self.height):
			for x in range(self.width):
				for c in self.buff[y][x]:
					print(c,end="")
			print()

	def clear(self):
		for y in range(self.height):
			for x in range(self.width):
				self.buff[y][x] = [Back.RESET,Fore.RESET," "]

		os.system("clear")

	def background(self,color):
		self.backgroundColor = self.colorEquivBack[color]

	def color(self,color):
		self.textColor = self.colorEquivFore[color]

	def setPixel(self,x,y,char=" "):
		x = int(x)
		y = int(y)
		if (x<self.width-1 and y<self.height and x>0 and y>0):
			self.buff[y][x] = [self.backgroundColor,self.textColor,char[0]]


	def drawString(self,x,y,text):
		for i in range(len(text)):
			self.setPixel(x+i,y,text[i])


	def run(self,setup,draw):
		setup()
		while not self.quit:
			draw()