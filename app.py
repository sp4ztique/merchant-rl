import libtcodpy as libtcod
import sys

import entity, maps, log

from globalconst import *

class App(object):
	def __init__(self):
		self.running  = True
		self.size     = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
		self.con = None
		self.entities = []
		self.drawing_mode = "normal"

	def on_init(self):
		# libtcod intialisation
		libtcod.console_set_custom_font("terminal8x8_aa_ro.png", libtcod.FONT_LAYOUT_ASCII_INROW)
		libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, "merchant-rl", False)
		libtcod.sys_set_fps(LIMIT_FPS)

		self.main_panel = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.bottom_panel = libtcod.console_new(self.width, BOTTOM_PANEL_HEIGHT)

		self.log = log.Log(self)

		print ""
		print "Merchant-rl -- pre-alpha -- v0.0"
		print "Made by sp4ztique"
		print ""

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
				elif keychar == "t" or keychar == "T":
					self.drawing_mode = "tiles"
				elif keychar == "n" or keychar == "N":
					self.drawing_mode = "normal"
				elif keychar == "h" or keychar == "H":
					self.drawing_mode = "temps"
				elif keychar == "r" or keychar == "R":
					self.drawing_mode = "rain"
		if ev == libtcod.EVENT_MOUSE_PRESS:
			x = mouse.cx
			y = mouse.cy
			print libtcod.heightmap_get_value(self.map.heightmap, x*2, y*2)
			for entity in self.entities:
				if entity.x == x and entity.y == y:
					entity.on_click()

	def on_loop(self):
		self.on_event()
		if libtcod.console_is_window_closed():
			self.running = False
	
	def on_render(self, flag):
		if flag == "clear":
			for entity in self.entities:
				entity.clear(self.main_panel)
		elif flag == "draw":
			self.map.draw(self.main_panel, mode = self.drawing_mode)

			for entity in self.entities:
				entity.draw(self.main_panel)

			self.log.draw(self.bottom_panel)

			libtcod.console_blit(self.main_panel, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
			libtcod.console_blit(self.bottom_panel, 0, 0, self.width, BOTTOM_PANEL_HEIGHT, 0, 0, MAP_HEIGHT)
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