import pyglet
from pyglet.window import key, FPSDisplay
import numpy as np

start_Window_width = 1200
start_Window_heigth = 800

class Attribute:
    def __init__(self, game):            
        self.game = game                                # Attribute knows game it's part of
        self.game.attributes.append(self)               # Game knows all its attributes
        self.install()                                  # Put in place graphical representation of attribute - 'children' must have install, which put
        self.reset()                                    # Reset attribute to start position - 'children' must have reset

    def reset (self):                                   # Restore starting positions or score, then commit to Pyglet
        self.commit ()                                   # Nothing to restore for the Attribute base class

    #def install(self):
    #    pass

    def predict (self):
        pass

    def interact (self):
        pass

    def commit (self):
        pass

    

class Sprite (Attribute):

    #defs: __init__(self+super), install, reset(self+super>commit), predict(self>later, super>pass), interact(super), commit(self>sync, super>pass)
    #all sprites have an image for these classes to work (may be changed later)
    def __init__ (self, game, img):
        self.img = img
        Attribute.__init__ (self, game)

    def install (self):                                         # The sprite holds a pygletSprite, that pyglet can display
        self.image = pyglet.image.load('res/sprites/'+self.img)
 
        self.width = self.image.width
        self.height = self.image.height
        self.image.anchor_x = self.width // 2                    # Middle of image is reference point
        self.image.anchor_y = self.height // 2
        self.anchor_x = self.image.anchor_x
        self.anchor_y = self.image.anchor_y
        
        self.pygletSprite = pyglet.sprite.Sprite (self.image, 0, 0, batch = self.game.batch)
        
    def reset (self, pos_x, pos_y, vel_x = 0, vel_y = 0):
        
        self.pos_x = pos_x-self.anchor_x                  # Start position, (can be commit, no bouncing initially?)
        self.pos_y = pos_y-self.anchor_y

        self.vel_x = vel_x                                      # Speed
        self.vel_y = vel_y
        
        Attribute.reset (self)

    
    def predict (self):                                         # Predict position, (do not yet commit, bouncing may alter it?)
        self.pos_x += self.vel_x * self.game.deltaT
        self.pos_y += self.vel_y * self.game.deltaT
    

    def commit (self):                                          # Update pygletSprite for asynch draw (position syncing)
        self.pygletSprite.x = self.pos_x
        self.pygletSprite.y = self.pos_y
 


class Player_Ship (Sprite):
    image = 'PlayerShip.png'
    margin = 100
    speed = 300
    player_fire = False
    #player_fire_rate = 0
    


    def __init__ (self, game):
        Sprite.__init__ (self, game, self.image)

    def reset (self):
        Sprite.reset(
            self,
            pos_x = start_Window_width//2 + self.anchor_x,                     
            pos_y = start_Window_heigth//6 + self.anchor_y)

    def predict (self):                                             # Let playership react on keys
        self.vel_y = 0
        
        if self.game.keymap [pyglet.window.key.RIGHT]:              # Right arrow pressed
            self.vel_x = self.speed
        elif self.game.keymap [pyglet.window.key.LEFT]:             # Left arrow pressed
            self.vel_x = -self.speed
        
        elif self.game.keymap [pyglet.window.key.SPACE]:
            self.player_fire = True


        elif not self.game.keymap [pyglet.window.key.RIGHT]:        # Right arrow released
            self.vel_x = 0
        elif not self.game.keymap [pyglet.window.key.LEFT]:         # Left arrow released
            self.vel_x = 0
        elif not self.game.keymap [pyglet.window.key.SPACE]:
            self.player_fire = False
        
                
        Sprite.predict (self)                           # Do not yet commit, playership may bounce with walls

    def interact (self):
        pos_x_max = start_Window_width - self.anchor_x - self.margin
        pos_x_min = self.anchor_x + self.margin

        if self.pos_x >= pos_x_max:
            self.pos_x = pos_x_max
        elif self.pos_x <= pos_x_min:
            self.pos_x = pos_x_min

        #if self.player_fire == True:

           
        #elif self.player_fire == False:
        #    pass


class Player_Laser (Sprite):
    image = 'laser.png'
    speed = 400
    margin = 100


    def __init__ (self, game, player_ship):
        self.player_ship = player_ship
        self.out_of_screen = False
        Sprite.__init__(self, game, self.image)

    def reset(self):
        Sprite.reset(
            self,
            pos_x = self.player_ship.pos_x,
            pos_y = self.player_ship.pos_y)

    def predict (self):
        self.vel_y = self.speed  
        
        Sprite.predict(self)

    def interact (self):
        pos_y_max = 400 #+ self.height + self.margin

        if self.pos_y >= pos_y_max:
            self.out_of_screen = True

        #print(self.out_of_screen, self.pos_y)



'''
class Space (Sprite):
    image = 'space.jpg'
    speed = -300

    def __init__ (self, game, index):
        self.index = index
        Sprite.__init__ (self, game, self.image)

    def reset (self):
        Sprite.reset(
            self,
            pos_x = start_Window_width,                         #anchorpoint will be deducted from pos_x so need to do full 
            pos_y = self.height+self.index*1200)

    def predict (self):
        self.vel_y = self.speed

        Sprite.predict(self)

    
    def interact (self):

        if self.pos_y <= -self.height-100:                                     #if pos 100 pixels below screen
            self.game.spaces.remove(self)                                                     #if bottom image is below screen, remove and create new image and add to list (see below)
            self.game.spaces.append()             #is this an elegant way to solve the scrolling (creating new background), is the list just growing?
    
'''
        

class Game:
    def __init__ (self):

        self.batch = pyglet.graphics.Batch ()                   # Graphical reprentations insert themselves for batch drawing

        self.deltaT = 0
        self.pause = True
        self.player_fire_rate = 0

        self.attributes = []
        #self.spaces = [Space (self, index) for index in range (2)]
        #print (self.spaces[0].pos_x, self.spaces[0].pos_y)
        #print (self.spaces[0].pygletSprite.x, self.spaces[0].pygletSprite.y)
        #print (self.spaces[1].pos_x, self.spaces[1].pos_y)
        #print (self.spaces[1].pygletSprite.x, self.spaces[1].pygletSprite.y)
        self.player_ship = Player_Ship(self)
        self.player_lasers = []
        

        self.window = pyglet.window.Window(1200, 800, visible=False, caption="Space Invaders", resizable=False)

        self.keymap = pyglet.window.key.KeyStateHandler ()  # Create keymap
        self.window.push_handlers (self.keymap)             # Install it as a handler

        self.window.on_draw = self.draw                     # Install draw callback, will be called asynch

        self.window.set_location (                          # Middle of the screen that it happens to be on
            (self.window.screen.width - self.window.width) // 2,
            (self.window.screen.height - self.window.height) // 2
        )

        self.window.clear ()
        self.window.flip ()                                 # Copy drawing buffer to window
        self.window.set_visible (True)                      # Show window once its contents are OK
        
        pyglet.clock.schedule_interval (self.update, 1/60.) # Install update callback to be called 60 times per s
        pyglet.app.run ()                                   # Start pyglet engine


    def update (self, deltaT):                              # Note that update and draw are not synchronized
        self.deltaT = deltaT                                # Actual deltaT may vary, depending on processor load
        
        
        if self.pause:                                      # If in paused state
            if self.keymap [pyglet.window.key.SPACE]:       #   If SPACEBAR hit
                self.pause = False                          #       Start playing
            #elif self.keymap [pyglet.window.key.ENTER]:     #   Else if ENTER hit
            #   self.scoreboard.reset ()                    #       Reset score
            elif self.keymap [pyglet.window.key.ESCAPE]:    #   Else if ESC hit
                self.exit ()                                #       End game
             
        else:                                               # Else, so if in active state
            for attribute in self.attributes:               #   Compute predicted values
                attribute.predict ()
                
            for attribute in self.attributes:               #   Correct values for bouncing and scoring
                attribute.interact ()
                
            for attribute in self.attributes:               #   Commit them to pyglet for display
                attribute.commit ()

            if self.player_ship.player_fire == True:
                self.player_fire_rate -= self.deltaT
                if self.player_fire_rate <= 0:
                    self.player_lasers.append(Player_Laser(self, self.player_ship))
                    self.player_fire_rate += 0.2

            for lsr in self.player_lasers:
                if lsr.out_of_screen == True:
                    self.player_lasers.remove(lsr)
        
        print(len(self.player_lasers))

        

    def draw (self):
        self.window.clear ()
        self.batch.draw ()      # All attributes added their graphical representation to the batch
         

game = Game()





'''
notes:
- playerfire won't stop

- add label if paused (press space to begin/continue)
- spaces: kijken of het wel zo goed gaat, want 1) index doorgeven bij nieuwe? 2)als je iets uit lijst verwijdert, shuif index ook op?

- player: gaat het wel goed met de andere kant op gaan met een ingestelde velocity


- uitzoeken hoe ik in player_ship window kan gebruiken (nu error dat ie niet herkent dat game een window attribute heeft) > nu maar gewoon pixels aangeven
'''








