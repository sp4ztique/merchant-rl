import libtcodpy as libtcod

class Entity(object):
	def __init__(self, owner, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.owner = owner

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def draw(self, con):
		libtcod.console_set_default_foreground(con, self.color)
		libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self, con):
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

	def on_click(self):
		self.owner.log.message("Entity clicked at (" + str(self.x) + ", " + str(self.y) + ")", self.color)

class City(Entity):
	def on_click(self):
		self.owner.log.message("City clicked at (" + str(self.x) + ", " + str(self.y) + ")", self.color)
		self.owner.log.message("Is coastal? " + str(self.is_coastal), self.color)

	def __init__(self, owner, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.owner = owner

		self.is_coastal = False

		# Check if near coast
		# tiles = owner.map.tiles
		# if tiles[x+1][y].terrain == "water":
		# 	self.is_coastal = True
		# elif tiles[x-1][y].terrain == "water":
		# 	self.is_coastal = True
		# elif tiles[x][y+1].terrain == "water":
		# 	self.is_coastal = True
		# elif tiles[x][y-1].terrain == "water":
		# 	self.is_coastal = True