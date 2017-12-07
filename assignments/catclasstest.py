class Cat:
	def __init__ (self, name, age):
		self.name = name
		self.age = age

	def speak (self):
		print('Miauw! I am', self.name, 'and I am', self.age, 'year(s) old!')

cat = Cat('Harry', 2)
cat.speak()