from display import Display
import time

if __name__ == "__main__":
	d = Display()

	def setup():
		print("Setup")
		d.i = 0

	def draw():
		d.i += 1
		i = d.i
		d.clear()
		d.color("blue")
		d.drawString(i*2,i,"Hello World")
		
		d.color("red")
		d.drawString((d.width-i-2),i,"Bonjour tout le monde")

		# d.background("blue")
		d.color("orange")
		d.setPixel(d.width/2,i,"O")

		d.drawBuffer()
		time.sleep(0.1)

	d.run(setup,draw)