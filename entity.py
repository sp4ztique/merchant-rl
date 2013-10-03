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