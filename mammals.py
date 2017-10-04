#### create a hierarchie of mammals ####

class Mammal:

	def __init__ (self, name):
		self.name = name

	def speak (self, name):
		print('Hi! I am', name)



class LandMammal (Mammal):

	def __init__ (self, name):
		super().__init__(name)

	def walk (self):
		print('Look at me, me is walking')


class AquaMammal (Mammal):

	def __init__ (self, name):
		super().__init__(name)

	def swim (self):
		print('Look at me, me is swimming')


class Cow (LandMammal):

	def __init__ (self, name):
		super().__init__(name)

	def graze (self):
		print('Look at me, me is grazing')


class Horse (LandMammal):

	def __init__ (self, name):
		super().__init__(name)

	def gallop (self):
		print('Look at me, me is galloping')


class Dolphin (AquaMammal):

	def __init__ (self, name):
		super().__init__(name)



class Shark (AquaMammal):

	def __init__ (self, name):
		super().__init__(name)


class Locomokipkachelfantje (LandMammal, AquaMammal):

	def __init__ (self, name):
		super().__init__(name)


