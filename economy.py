class Agent(object):
	# An agent in a cities economy
	# Can buy resources and sell products
	# Will also buy food
	def __init__(self, owner):
		self.owner = owner