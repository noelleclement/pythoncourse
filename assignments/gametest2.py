import pyglet

class Attribute:                        # Attribute in the gaming sense of the word, rather than of an object
    def __init__ (self, game):
        self.game = game                    # Attribute knows game it's part of
        self.game.attributes.append (self)  # Game knows all its attributes
        self.install ()                     # Put in place graphical representation of attribute
        self.reset ()                       # Reset attribute to start position
                    
    def reset (self):       # Restore starting positions or score, then commit to Pyglet
        self.commit ()      # Nothing to restore for the Attribute base class
                
    def predict (self):
        pass
                
    def interact (self):
        pass
        
    def commit (self):
        pass

class Sprite(Attribute):
    def __init__ (self, game, width, height):
        self.width = width
        self.height = height
        Attribute.__init__ (self, game)
        
    def install (self):     # The sprite holds a pygletSprite, that pyglet can display
        image = pyglet.image.create (
            self.width,
            self.height,
            pyglet.image.SolidColorImagePattern ((255, 255, 255, 255))  # RGBA
        )
 
        image.anchor_x = self.width // 2    # Middle of image is reference point
        image.anchor_y = self.height // 2
        
        self.pygletSprite = pyglet.sprite.Sprite (image, 0, 0, batch = self.game.batch)
        

class Kart(Sprite):
    def __init__(self, game, width, height):
        Sprite.__init__(self, game, width, height)

    def predict (self): # Let kart react on keys
        
        if self.index:  # Right player
            if self.game.keymap [pyglet.window.key.left]:  # Letter K pressed
                self.vY = self.speed
            elif self.game.keymap [pyglet.window.key.M]:
                self.vY = -self.speed
        else:           # Left player
            if self.game.keymap [pyglet.window.key.A]:
                self.vY = self.speed
            elif self.game.keymap [pyglet.window.key.Z]:
                self.vY = -self.speed
                
        Sprite.predict (self)   # Do not yet commit, paddle may bounce with walls



class Game:
    def __init__ (self):
        self.batch = pyglet.graphics.Batch ()   # Graphical reprentations insert themselves for batch drawing
        
        self.deltaT = 0                             # Elementary timestep of simulation
                        
        self.window = pyglet.window.Window (                # Main window
            640, 480, resizable = True, visible = False, caption = "Game"
        )
        
        self.window.on_draw = self.draw                     # Install draw callback, will be called asynch
        
        self.window.set_location (                          # Middle of the screen that it happens to be on
            (self.window.screen.width - self.window.width) // 2,
            (self.window.screen.height - self.window.height) // 2
        )

        self.label = pyglet.text.Label('Hello, world',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=self.window.width//2, y=self.window.height//2,
                                  anchor_x='center', anchor_y='center',
                                  batch=self.batch)
        
        self.window.clear ()
        self.window.flip ()                                 # Copy drawing buffer to window
        self.window.set_visible (True)                      # Show window once its contents are OK
        
        pyglet.app.run () 

    def draw (self):
        self.window.clear ()
        self.batch.draw ()      # All attributes added their graphical representation to the batch

    def update (self, deltaT):                              # Note that update and draw are not synchronized
        self.deltaT = deltaT                                # Actual deltaT may vary, depending on processor load
    
        if self.pause:                                      # If in paused state
            if self.keymap [pyglet.window.key.SPACE]:       #   If SPACEBAR hit
                self.pause = False                          #       Start playing
            elif self.keymap [pyglet.window.key.ENTER]:     #   Else if ENTER hit
                self.scoreboard.reset ()                    #       Reset score
            elif self.keymap [pyglet.window.key.ESCAPE]:    #   Else if ESC hit
                self.exit ()                                #       End game
                
        else:                                               # Else, so if in active state
            for attribute in self.attributes:               #   Compute predicted values
                attribute.predict ()
                
            for attribute in self.attributes:               #   Correct values for bouncing and scoring
                attribute.interact ()
                
            for attribute in self.attributes:               #   Commit them to pyglet for display
                attribute.commit ()
            

game = Game()