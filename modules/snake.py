import copy

class point:
	def __init__(self,x,y):
		self.x = x
		self.y = y


class Snake:
	def __init__(self,x,y,size=2):
		self.points = list()
		self.points.append(point(x,y))
		self.direction = 1
		self.keyToDir = {
			"z":0,
			"d":1,
			"s":2,
			"q":3
		}
		self.addPoint = False
		for i in range(size):
			self.points.append(point(x+i,y))


	def moove(self):
		if not self.addPoint:
			for i in range(0,len(self.points)-1):
				self.points[i] = copy.deepcopy(self.points[i+1])
		else:
			p = copy.deepcopy(self.points[-1])
			self.points.append(p)
			self.addPoint = False

		if (self.direction == 0):
			self.points[-1].y -= 1
		elif (self.direction == 1):
			self.points[-1].x += 1
		elif (self.direction == 2):
			self.points[-1].y += 1
		elif (self.direction == 3):
			self.points[-1].x -= 1

	def draw(self,display):
		for i in range(len(self.points)):
			display.color("white")
			if (i == len(self.points)-1):
				display.background("green")
				display.setPixel(self.points[i].x,self.points[i].y,"X")
			else:
				display.background("lightgreen")
				display.setPixel(self.points[i].x,self.points[i].y,"0")

	def setPos(self,key):
		if (key in self.keyToDir):
			if (self.keyToDir[key] != self.direction):
				self.direction = self.keyToDir[key]

	def walls(self,width,height):
		if(self.points[-1].x < 0 or self.points[-1].x>width-1 or self.points[-1].y<0 or self.points[-1].y>height-1):
			return True

	def apple(self,point):
		return self.points[-1].x == point.x and self.points[-1].y == point.y

	def add(self):
		self.addPoint = True