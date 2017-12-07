#### create a hierarchy of mammals ####

class Mammal:

    def __init__ (self, name):
        self.name = name

    def speak (self):
        print('Hi! I am', self.name)



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

    def playing (self):
        print('Look at me, me is playing')


class Shark (AquaMammal):

    def __init__ (self, name):
        super().__init__(name)

    def fishAreFriends (self):
        print('Repeat after me: Fish are friends, not food')

class Locomokipkachelfantje (LandMammal, AquaMammal):

    def __init__ (self, name):
        super().__init__(name)

    def fanting (self):
        print('Look at me, me is fanting. Fant fant.')

mammals = [Cow('Marjo'), Horse('Henk'), Dolphin('Judy'), Shark('Marvin'), Locomokipkachelfantje('Henry')]

for mammal in mammals:
    mammal.speak()
