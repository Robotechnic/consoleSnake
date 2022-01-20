from modules.display import Display
from modules.snake import *
import time
from random import randint

if __name__ == "__main__":
	d = Display()

	def changeGame(gameType):
		d.gameDisplay = gameType

	def setup():
		d.snake = Snake(2, 3)
		d.gameDisplay = "menu"

		d.gameMenu = [
			[
				" ____  __      __   _  _ \n(  _ \(  )    /__\ ( \/ )\n )___/ )(__  /(__)\ \  / \n(__)  (____)(__)(__)(__) ",
				lambda: changeGame("game"),
			],
			[
				" ____  _  _  ____  ____ \n( ___)( \/ )(_  _)(_  _)\n )__)  )  (  _)(_   )(  \n(____)(_/\_)(____) (__) ",
				lambda: d.exit(),
			],
		]

		d.gameSelection = 0
		d.apple = point(randint(0,d.width),randint(0,d.height))

	def draw():
		d.clear()

		if d.gameDisplay == "game":
			d.color("white")
			d.background("green")

			d.snake.moove()
			d.snake.draw(d)
			if d.snake.walls(d.width, d.height):
				d.gameDisplay = "gameOver"

			if (d.snake.apple(d.apple)):
				d.snake.add()
				d.apple = point(randint(0,d.width),randint(0,d.height))

			d.background("black")
			d.color("red")

			d.drawString(1, 1, str(len(d.snake.points)))

			d.background("black")
			d.color("yellow")

			d.centerString(1,"Press c to exit or e to return to main screen")

			d.background("red")
			d.color("white")
			d.drawString(d.apple.x,d.apple.y,"@")
		elif d.gameDisplay == "menu":
			d.color("white")
			d.centerString(
				1,
				"  ___  _____  _  _  ___  _____  __    ____    ___  _  _    __    _  _  ____ \n / __)(  _  )( \( )/ __)(  _  )(  )  ( ___)  / __)( \( )  /__\  ( )/ )( ___)\n( (__  )(_)(  )  ( \__ \ )(_)(  )(__  )__)   \__ \ )  (  /(__)\  )  (  )__) \n \___)(_____)(_)\_)(___/(_____)(____)(____)  (___/(_)\_)(__)(__)(_)\_)(____)",
			)
			for i in range(len(d.gameMenu)):
				if i == d.gameSelection:
					d.background("green")
				else:
					d.background("black")
				d.centerString(int(7 + i * 5), d.gameMenu[i][0])

		elif d.gameDisplay == "gameOver":
			d.color("red")
			d.centerString(
				5,
				"   ____                         ___                        __\n  / ___| __ _ _ __ ___   ___   / _ \__   _____ _ __   _   / /\n | |  _ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__| (_) | | \n | |_| | (_| | | | | | |  __/ | |_| |\ V /  __/ |     _  | | \n  \____|\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|    ( ) | | \n                                                     |/   \_\\",
			)

		d.background("black")

		time.sleep(0.1)

	def keyPressed(key):
		if d.gameDisplay == "menu":
			if key == "c":
				d.exit()
			elif key == "z":
				d.gameSelection = 0
			elif key == "s":
				d.gameSelection = 1
			elif key == " ":
				d.gameMenu[d.gameSelection][1]()
		elif d.gameDisplay == "game":
			d.snake.setPos(key)

			if (key == "e"):
				d.gameDisplay = "menu"
				d.snake = Snake(2, 3)
		elif d.gameDisplay == "gameOver" and key == " ":
			d.snake = Snake(2, 3)
			d.gameDisplay = "menu"

	d.run(setup, draw, keyPressed)
