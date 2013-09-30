#!/usr/bin/python2

import libtcodpy as libtcod
import sys

import app, maps
from globalconst import *

# Start the game
if __name__ == "__main__":
	game = app.App()
	game.on_execute()