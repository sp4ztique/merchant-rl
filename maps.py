from globalconst import *
import libtcodpy as libtcod

class Map:
	def __init__(self, owner, width = MAP_WIDTH, height = MAP_HEIGHT, gen = True):
		self.size = self.width, self.height = width, height
		self.owner = owner
		self.generated = False

		self.image = libtcod.image_new(self.width * 2, self.height * 2)
		for x in range(self.width*2):
			for y in range(self.height*2):
				col = libtcod.random_get_int(0, 0, 255)
				libtcod.image_put_pixel(self.image, x, y, libtcod.Color(col, col, col))
		
		if gen:
			self.generate()

	def generate(self):
		print "Generating map..."
		noise = libtcod.noise_new(2, 0.5, 2.0)
		heightmap = libtcod.heightmap_new(2*self.width, 2*self.height)
		maxi = 0
		mini = 0

		print "-- heightmap..."
		for x in range(self.width*2):
			for y in range(self.height*2):
				f = [3 * float(x) / (2*self.width), 3 * float(y) / (2*self.height)]
				value = (libtcod.noise_get_fbm(noise, f, 4, libtcod.NOISE_PERLIN))/2
				if value > maxi:
					maxi = value
				if value < mini:
					mini = value
				libtcod.heightmap_set_value(heightmap, x, y, value)

		# print "-- erode the map"
		# libtcod.heightmap_rain_erosion(heightmap, self.width*2*self.height*2*2,0.1,0.3)

		deep = libtcod.Color(1, 10, 27)
		mid = libtcod.Color(38, 50, 60)
		shallow = libtcod.Color(51, 83, 120)
		water_idx = [0, 190, 255]
		water_cols = [deep, mid, shallow]
		water_colormap = libtcod.color_gen_map(water_cols, water_idx)


		mountaintop = libtcod.Color(145, 196, 88)
		grass = libtcod.Color(40, 62, 19)
		foothill = libtcod.Color(57, 81, 34)
		sand = libtcod.Color(215, 185, 115)
		watersedge = libtcod.Color(19, 97, 101)

		land_idx = [0, 15, 20, 128, 255]
		land_cols = [watersedge, sand, grass, foothill, mountaintop]
		land_colormap = libtcod.color_gen_map(land_cols, land_idx)

		print "-- paint the image and normalize the heights..."
		self.heightmap = libtcod.heightmap_new(self.width*2, self.height*2)

		for x in range(self.width*2):
			for y in range(self.height*2):
				value = libtcod.heightmap_get_value(heightmap, x, y)
				if value < 0:
					value += 1
					mini2 = mini + 1
					coeff = (value - mini2)/(1-mini2)
					index = int(coeff * 255)
					libtcod.image_put_pixel(self.image, x, y, water_colormap[index])
					libtcod.heightmap_set_value(self.heightmap, x, y, -coeff)
				else:
					value = value / maxi
					index = int(value * 255)
					libtcod.image_put_pixel(self.image, x, y, land_colormap[index])
					libtcod.heightmap_set_value(self.heightmap, x, y, value)

		print "-- apply normal shadows"
		for x in range(self.width*2):
			for y in range(self.height*2):
				normal = libtcod.heightmap_get_normal(self.heightmap, x, y, -1)
				nx = normal[0]
				ny = normal[1]
				avg = (nx + ny)/2
				if avg > 0:
					avg = 1
				else:
					avg = avg + 1
					avg = avg/2 + 0.5
				col = libtcod.image_get_pixel(self.image, x, y) * avg
				libtcod.image_put_pixel(self.image, x, y, col)

		print "Map generated"

	def draw(self, con):
		libtcod.image_blit_2x(self.image, con, 0, 0)