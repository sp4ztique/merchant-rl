import textwrap
import libtcodpy as libtcod

from globalconst import *

class Log:
	def __init__(self, owner):
		self.messages = []
		self.history = []
		self.owner = owner

	def message(self, msg, colour = libtcod.white, debug = False):
		msg_lines = textwrap.wrap(msg, MSG_WIDTH)

		for line in msg_lines:
			if len(self.messages) == MSG_HEIGHT:
				del self.messages[0]

			self.messages.append((line, colour))
			self.history.append((line, colour))

		if debug:
			self.draw(self.owner.bottom_panel)
			libtcod.console_blit(self.owner.bottom_panel, 0, 0, self.owner.width, BOTTOM_PANEL_HEIGHT, 0, 0, MAP_HEIGHT)
			libtcod.console_flush()

	def draw(self, con):
		y = 1
		for (line, colour) in self.messages:
			for x in range(MSG_WIDTH):
				libtcod.console_put_char(con, x + MSG_X, y, ' ', libtcod.BKGND_NONE)
			libtcod.console_set_default_foreground(con, colour)
			libtcod.console_print_ex(con, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
			y += 1

	def dump_history(self):
		print "==Dumping log history:"
		for line, colour in self.history:
			print line
		print "==Done."