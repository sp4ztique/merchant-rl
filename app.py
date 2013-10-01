import libtcodpy as libtcod
import sys

import entity, maps

from globalconst import *

class App:
	def __init__(self):
		self.running  = True
		self.size     = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
		self.con = None
		self.entities = []

	def on_init(self):
		# libtcod intialisation
		libtcod.console_set_custom_font("terminal12x12_gs_ro.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
		libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, "merchant-rl", False)
		libtcod.sys_set_fps(LIMIT_FPS)
		self.con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

		self.map = maps.Map(self)

		self.running = True		

	def on_event(self):
		key = libtcod.Key()
		mouse = libtcod.Mouse()
		ev = libtcod.sys_check_for_event(libtcod.EVENT_ANY, key, mouse)
		if ev == libtcod.EVENT_KEY_PRESS:
			if key.vk == libtcod.KEY_ESCAPE:
				self.running = False
			elif key.vk == libtcod.KEY_CHAR:
				keychar = chr(key.c)
				if keychar == "g" or keychar == "G":
					self.map.generate()

		if ev == libtcod.EVENT_MOUSE_PRESS:
			x = mouse.cx
			y = mouse.cy
			normal = libtcod.heightmap_get_normal(self.map.heightmap, x*2, y*2, 0)
			print normal

	def on_loop(self):
		self.on_event()
		if libtcod.console_is_window_closed():
			self.running = False
	
	def on_render(self, flag):
		if flag == "clear":
			for entity in self.entities:
				entity.clear(self.con)
		elif flag == "draw":
			self.map.draw(self.con)
			for entity in self.entities:
				entity.draw(self.con)
			libtcod.console_blit(self.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
			libtcod.console_flush()
		else:
			print "Invalid flag passed to App.on_render: " + flag
			running = False

	def on_cleanup(self):
		sys.exit()

	def on_execute(self):
		if self.on_init() == False:
			self.running = False
		self.on_render("draw")
		while(self.running):
			self.on_render("draw")
			self.on_loop()
			self.on_render("clear")			
		self.on_cleanup()