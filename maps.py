from globalconst import *
import libtcodpy as libtcod
import entity, sys

class Tile(object):
	def __init__(self, terrain = "land"):
		self.terrain = terrain
		self.owned_by = None
		self.char = None
		self.fg_color = None
		self.info = "No info available"
		self.temp = 0
		self.rain = 0

class Map(object):
	def __init__(self, owner, width = MAP_WIDTH, height = MAP_HEIGHT, gen = True):
		self.size = self.width, self.height = width, height
		self.owner = owner
		self.generated = False

		self.tiles = [[ Tile()
			for y in range(self.height) ]
				for x in range(self.width) ]

		self.image = libtcod.image_new(self.width * 2, self.height * 2)
		
		if gen:
			self.generate()

	def generate(self):
		self.owner.log.message("Generating map...", debug = True)
		noise = libtcod.noise_new(2, 0.5, 2.0)
		heightmap = libtcod.heightmap_new(2*self.width, 2*self.height)
		maxi = 0
		mini = 0

		self.tiles = [[ Tile()
			for y in range(self.height) ]
				for x in range(self.width) ]

		self.owner.log.message("-- creating heightmap...", debug = True)
		for x in range(self.width*2):
			for y in range(self.height*2):
				f = [3 * float(x) / (2*self.width), 3 * float(y) / (2*self.height)]
				value = (libtcod.noise_get_fbm(noise, f, 5, libtcod.NOISE_PERLIN))/2
				if value > maxi:
					maxi = value
				if value < mini:
					mini = value
				libtcod.heightmap_set_value(heightmap, x, y, value)

		# print "-- erode the map"
		# libtcod.heightmap_rain_erosion(heightmap, self.width*2*self.height*2*2,0.1,0.2)

		deep = libtcod.Color(1, 10, 27)
		mid = libtcod.Color(38, 50, 60)
		shallow = libtcod.Color(51, 83, 120)
		water_idx = [0, 70, 210, 255]
		water_cols = [deep, deep, mid, shallow]
		water_colormap = libtcod.color_gen_map(water_cols, water_idx)


		mountaintop = libtcod.Color(145, 196, 88)
		grass = libtcod.Color(40, 62, 19)
		foothill = libtcod.Color(57, 81, 34)
		sand = libtcod.Color(215, 185, 115)
		watersedge = libtcod.Color(19, 97, 101)

		land_idx = [0, 15, 20, 128, 255]
		land_cols = [watersedge, sand, grass, foothill, mountaintop]
		land_colormap = libtcod.color_gen_map(land_cols, land_idx)

		self.owner.log.message("-- paint the image and normalize the heights...", debug = True)
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

		self.owner.log.message("-- apply normal shadows", debug = True)
		for x in range(self.width*2):
			for y in range(self.height*2):
				normal = libtcod.heightmap_get_normal(self.heightmap, x, y, 0)
				nx = normal[0]
				ny = normal[1]
				avg = (nx + ny)/2
				if avg > 0:
					avg = 1
				else:
					avg = avg + 1
					avg = min(avg/2 + 0.5, 1)
				col = libtcod.image_get_pixel(self.image, x, y) * avg 
				libtcod.image_put_pixel(self.image, x, y, col)

		self.owner.log.message("-- setting up tiles", debug = True)
		for x in range(self.width):
			for y in range(self.height):
				h = libtcod.heightmap_get_value(self.heightmap, x*2, y*2)
				if h >= 0.05:
					self.tiles[x][y].terrain = "land"
				else:
					self.tiles[x][y].terrain = "water"

		self.owner.log.message("-- creating temperature map", debug = True)
		noise2 = libtcod.noise_new(2, 0.5, 2.0)
		temp_max = 0
		temp_min = 1
		for x in range(self.width):
			for y in range(self.height):
		 		f = [3 * float(x) / (self.width), 3 * float(y) / (self.height)]
	 			value = (libtcod.noise_get_fbm(noise2, f, 5, libtcod.NOISE_PERLIN))/2
	 			value = (value + 1)/2
	 			if value < temp_min:
	 				temp_min = value
	 			if value > temp_max:
	 				temp_max = value
				self.tiles[x][y].temp = value

		temp_max = temp_max - temp_min

		for x in range(self.width):
			for y in range(self.height):
				self.tiles[x][y].temp = (self.tiles[x][y].temp - temp_min)/temp_max

		self.owner.log.message("-- creating rainfall map", debug = True)
		noise3 = libtcod.noise_new(2, 0.5, 2.0)
		rain_max = 0
		rain_min = 1
		for x in range(self.width):
			for y in range(self.height):
		 		f = [3 * float(x) / (self.width), 3 * float(y) / (self.height)]
	 			value = (libtcod.noise_get_fbm(noise3, f, 5, libtcod.NOISE_PERLIN))/2
	 			value = (value + 1)/2
	 			if value < rain_min:
	 				rain_min = value
	 			if value > rain_max:
	 				rain_max = value
				self.tiles[x][y].rain = value

		rain_max = rain_max - rain_min

		for x in range(self.width):
			for y in range(self.height):
				self.tiles[x][y].rain = (self.tiles[x][y].rain - rain_min)/rain_max

		self.owner.log.message("Terrain complete", debug = True)

		self.owner.log.message("Placing cities", debug=True)

		self.owner.entities = []

		max_cities = 10
		num_cities = 0
		for i in range(max_cities):
			x = libtcod.random_get_int(0, 0, self.width - 1)
			y = libtcod.random_get_int(0, 0, self.height - 1)
			if self.tiles[x][y].terrain == "land":
				city = entity.City(self.owner, x, y, '#', libtcod.Color(libtcod.random_get_int(0, 0, 255), libtcod.random_get_int(0, 0, 255), libtcod.random_get_int(0, 0, 255)))
				self.owner.entities.append(city)
				num_cities += 1
		self.owner.log.message("-- placed " + str(num_cities) + " cities")

		self.owner.log.message("Map generated", debug = True)
		self.generated = True

	def draw(self, con, mode):
		if mode == "normal":
			libtcod.image_blit_2x(self.image, con, 0, 0)
			for x in range(self.width):
				for y in range(self.height):
					tile = self.tiles[x][y]
					if tile.char is not None:
						libtcod.console_set_default_foreground(con, tile.fg_color)
						libtcod.console_put_char(con, x, y, tile.char, libtcod.BKGND_NONE)
		elif mode == "tiles":
			for x in range(self.width):
				for y in range(self.height):
					if self.tiles[x][y].terrain == "land":
						libtcod.console_set_default_background(con, libtcod.Color(40, 62, 19))
						libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_SET)
					elif self.tiles[x][y].terrain == "water":
						libtcod.console_set_default_background(con, libtcod.Color(38, 50, 60))
						libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_SET)
		elif mode == "temps":
			cols = [libtcod.green, libtcod.yellow, libtcod.red]
			col_idx = [0, 50, 100]
			col_map = libtcod.color_gen_map(cols, col_idx)
			for x in range(self.width):
				for y in range(self.height):
					libtcod.console_set_default_foreground(con, col_map[int(self.tiles[x][y].temp*100)])
					libtcod.console_put_char(con, x, y, 'o', libtcod.BKGND_NONE)
		elif mode == "rain":
			cols = [libtcod.yellow, libtcod.green, libtcod.blue]
			col_idx = [0, 50, 100]
			col_map = libtcod.color_gen_map(cols, col_idx)
			for x in range(self.width):
				for y in range(self.height):
					libtcod.console_set_default_foreground(con, col_map[int(self.tiles[x][y].rain*100)])
					libtcod.console_put_char(con, x, y, 'o', libtcod.BKGND_NONE)
		else:
			print "Invalid drawing mode passed to Map.draw: " + mode
			sys.exit(1)