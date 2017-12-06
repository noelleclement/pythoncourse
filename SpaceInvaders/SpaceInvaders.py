import pyglet
from pyglet.window import key, FPSDisplay
from pyglet.gl import *
import numpy as np
import time
import gc 

start_Window_width = 1200
start_Window_height = 800


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
    has_image = False
    has_anim = False
    spr_image = None
    width = 0
    height = 0
    anchor_x = 0
    anchor_y = 0

    #defs: __init__(self+super), install, reset(self+super>commit), predict(self>later, super>pass), interact(super), commit(self>sync, super>pass)
    #all sprites have an image for these classes to work (may be changed later)
    def __init__ (self, game, img=None, anim=None):
        #self.img = img
        if img is not None:
            self.spr_image = pyglet.image.load('res/sprites/'+img)
            self.has_image = True

        elif anim is not None:
            self.spr_image = anim
            self.has_anim = True
        
        Attribute.__init__ (self, game)

    def install (self):                                         # The sprite holds a pygletSprite, that pyglet can display
        #self.image = pyglet.image.load('res/sprites/'+self.img)
 
        if self.has_image: #and not type(self.image) == str
            self.width = self.spr_image.width
            self.height = self.spr_image.height
            self.spr_image.anchor_x = self.width // 2                    # Middle of image is reference point
            self.spr_image.anchor_y = self.height // 2 
            self.anchor_x = self.spr_image.anchor_x
            self.anchor_y = self.spr_image.anchor_y

        
        elif self.has_anim:
            self.width = self.spr_image.get_max_width()
            self.height = self.spr_image.get_max_height()
            self.spr_image.anchor_x = self.width // 2
            self.spr_image.anchor_y = self.height // 2
            self.anchor_x = self.spr_image.anchor_x
            self.anchor_y = self.spr_image.anchor_y
        
        self.pygletSprite = pyglet.sprite.Sprite (self.spr_image, 0, 0, batch = self.game.batch)
        
    def reset (self, pos_x, pos_y, vel_x = 0, vel_y = 0):
        
        self.pos_x = pos_x #-self.anchor_x                  # Start position, (can be commit, no bouncing initially?)
        self.pos_y = pos_y #-self.anchor_y

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
    ps_image = 'PlayerShip.png'
    margin = 100
    speed = 300
    player_fire = False
    player_fire_rate = 0
    


    def __init__ (self, game):
        Sprite.__init__ (self, game, img = self.ps_image)

    def reset (self):
        Sprite.reset(
            self,
            pos_x = start_Window_width//2, # + self.anchor_x,                     
            pos_y = start_Window_height//6) # + self.anchor_y)

        #print(self.anchor_x)

    def predict (self):                                             # Let playership react on keys
        self.vel_y = 0
        
        if self.game.keymap [pyglet.window.key.RIGHT]:              # Right arrow pressed
            self.vel_x = self.speed
        elif self.game.keymap [pyglet.window.key.LEFT]:             # Left arrow pressed
            self.vel_x = -self.speed

        elif not self.game.keymap [pyglet.window.key.RIGHT]:        # Right arrow released
            self.vel_x = 0
        elif not self.game.keymap [pyglet.window.key.LEFT]:         # Left arrow released
            self.vel_x = 0
        
        if self.game.keymap [pyglet.window.key.SPACE]:
            self.player_fire = True

        elif not self.game.keymap [pyglet.window.key.SPACE]:
            self.player_fire = False
                
        Sprite.predict (self)                           # Do not yet commit, playership may bounce with walls

    def interact (self):
        pos_x_max = self.game.window.width - self.anchor_x - self.margin
        pos_x_min = self.anchor_x + self.margin

        if self.pos_x >= pos_x_max:
            self.pos_x = pos_x_max
        elif self.pos_x <= pos_x_min:
            self.pos_x = pos_x_min

        if self.player_fire:
            self.player_fire_rate -= self.game.deltaT
            if self.player_fire_rate <= 0:
                self.game.attributes.append(Player_Laser(self.game, self))
                self.player_fire_rate += 0.2

           
        elif self.player_fire == False:
            pass


class Player_Laser (Sprite):
    pl_image = 'laser.png'
    speed = 400
    margin = 100


    def __init__ (self, game, player_ship):
        self.player_ship = player_ship
        #self.out_of_screen = False
        Sprite.__init__(self, game, img = self.pl_image)

    def reset(self):
        Sprite.reset(
            self,
            pos_x = self.player_ship.pos_x, #+self.anchor_x,
            pos_y = self.player_ship.pos_y+self.player_ship.anchor_y)

    def predict (self):
        self.vel_y = self.speed  
        
        Sprite.predict(self)

      
    def interact (self):
        pos_y_max =  self.game.window.height + self.height + self.margin
        #low_y_enemy_ship = item.pos_y-item.anchor_y
        #hig_y_enemy_ship = item.pos_y+item.anchor_y
        #lef_x_enemy_ship = self.game.enemy_ship.pos_x#-self.game.enemy_ship.anchor_x
        #rig_x_enemy_ship = self.game.enemy_ship.pos_x+self.game.enemy_ship.width
        
        '''
        
        print('pos y enship: '+str(self.game.enemy_ship.pos_y))
        print(self.game.enemy_ship.anchor_y)
        print(self.game.enemy_ship.pos_x)
        print(self.game.enemy_ship.anchor_x)
        print('anchorx en ship: '+str(self.game.enemy_ship.anchor_x))

        print('pos y laser: '+str(self.pos_y))
        print(self.anchor_y)
        print(self.pos_x)
        print(self.anchor_x)

        print('pos y player: '+str(self.game.player_ship.pos_y))
        print(self.game.player_ship.anchor_y)
        print(self.game.player_ship.pos_x)
        print(self.game.player_ship.anchor_x)
        

        
        if self.pos_y > low_y_enemy_ship and self.pos_y < hig_y_enemy_ship:
            print('y is geraakt op '+ str(self.pos_y) )
            if self.pos_x > lef_x_enemy_ship and self.pos_x < rig_x_enemy_ship:
            #self.game.attributes.remove()
                print('x is geraaktttt op '+ str(self.pos_x))
        
        
        for item in self.game.attributes:
            if type(item) is Enemy_Ship:
                if self.pos_y > (item.pos_y) and self.pos_y < (item.pos_y+item.height):
                   print('y is geraakt op '+ str(self.pos_y) )
                   if self.pos_x > (item.pos_x) and self.pos_x < (item.pos_x+item.width):
                        print('x is geraaktttt op '+ str(self.pos_x))
                        self.game.attributes.remove(item)
                        #time.sleep(0.5)
                        #print(len(self.game.attributes))
                        #del item
        '''         

        if self.pos_y >= pos_y_max:
            #self.out_of_screen = True
            self.game.attributes.remove(self)
            self.pygletSprite.batch = None

        #print(self.out_of_screen, self.pos_y)
    

class Enemy_Ship(Sprite):
    enemy_ship = pyglet.image.load('res/sprites/enemyShip_Sh01.png')
    enemy_ship_seq = pyglet.image.ImageGrid(enemy_ship, 1, 15, item_width=100, item_height=100)
    enemy_ship_texture = pyglet.image.TextureGrid(enemy_ship_seq)
    enemy_ship_anim = pyglet.image.Animation.from_image_sequence(enemy_ship_texture[0:], 0.1, loop=True)
    
    speed = 100
    margin = 100
    enemy_fire_rate = 0

    def __init__(self, game):
        Sprite.__init__(self, game, anim=self.enemy_ship_anim)

    def reset (self):
        Sprite.reset(
            self,
            pos_x = np.random.randint (low=100, high=(start_Window_width-self.width-self.margin)), #start_Window_width//2, - self.anchor_x,                     
            pos_y = np.random.randint (low=(start_Window_height//2), high=(start_Window_height-self.margin)), # - self.anchor_y)
            vel_x = self.speed,
            vel_y = 0
        )
        #print(self.pos_x)



    def interact (self):
        pos_x_max = self.game.window.width - self.margin - self.width
        pos_x_min = self.margin

        
        if self.pos_x >= pos_x_max:
            self.vel_x = -self.speed
        elif self.pos_x <= pos_x_min:
            self.vel_x = self.speed
        
        for item in self.game.attributes:
            if type(item) is Player_Laser:
                if item.pos_y > (self.pos_y) and item.pos_y < (self.pos_y+self.height) and item.pos_x > (self.pos_x) and item.pos_x < (self.pos_x+self.width):
                    #print('y is geraakt op '+ str(self.pos_y) )
                    #print('x is geraaktttt op '+ str(self.pos_x))
                    self.game.attributes.remove(item)
                    item.pygletSprite.batch = None
                    self.game.attributes.remove(self)
                    self.game.enemy_ships.remove(self)
                    self.pygletSprite.batch = None
                    self.game.enemy_ships.append(Enemy_Ship(self.game))
                    self.game.scoreboard.score_increment()
                    
                    #print('attributes:')
                    #print(self.game.attributes)
                    #print('enemy_ships:')
                    #print(self.game.enemy_ships)


        self.enemy_fire_rate -= self.game.deltaT
        if self.enemy_fire_rate <= 0:
            if np.random.randint(0, 10) >= 5:
                self.game.attributes.append(Enemy_Laser(self.game, self))
                self.enemy_fire_rate += 0.2

                   
 
class Enemy_Laser(Sprite):
    el_image = 'enemy_laser.png'
    speed = 400
    margin = 100


    def __init__ (self, game, enemy_ship):
        self.enemy_ship = enemy_ship
        Sprite.__init__(self, game, img = self.el_image)

    def reset(self):
        Sprite.reset(
            self,
            pos_x = self.enemy_ship.pos_x+self.enemy_ship.anchor_x, 
            pos_y = self.enemy_ship.pos_y)

    def predict (self):
        self.vel_y = -self.speed  
        Sprite.predict(self)

    def interact(self):
        for item in self.game.attributes:
            if type(item) is Player_Ship:
                if self.pos_y < (item.pos_y+item.anchor_y) and self.pos_y >(item.pos_y-item.anchor_y) and self.pos_x > (item.pos_x-item.anchor_x) and self.pos_x < (item.pos_x+item.anchor_x):
                    #print('y is geraakt op '+ str(self.pos_y) )
                    #print('x is geraaktttt op '+ str(self.pos_x))
                    self.game.attributes.remove(self)
                    self.pygletSprite.batch = None
                    self.game.scoreboard.lives_decrement()

        if self.pos_y <= 80:
                #self.out_of_screen = True
                self.game.attributes.remove(self)
                self.pygletSprite.batch = None

                        
        

class Scoreboard (Attribute):

    def install (self): 

        def defineLabel (text, x, y):
            return pyglet.text.Label (
                text,
                font_name = 'Arial', font_size = 24,
                x = x, y = y,
                anchor_x = 'center', anchor_y = 'center',
                batch = self.game.batch
            )
    
        defineLabel ('Player Lives', 1*start_Window_width//4, 60)    # Player name
        defineLabel ('Player Score', 3*start_Window_width//4, 60)
 
        self.playerLives_label = defineLabel ('000', 1*start_Window_width//4, 30)
        self.playerScore_label = defineLabel ('000', 3*start_Window_width//4, 30)
        
 
        #self.game.batch.add (2, GL_LINES, None, ('v2i', (0, start_Window_height, start_Window_width, start_Window_height))) # Line
        
    def score_increment (self):
        self.playerScore += 25

    def lives_decrement (self):
        self.playerLives -= 1

        if self.playerLives <=0:
            self.game.game_over()
    
    def reset (self):
        self.playerScore = 0
        self.playerLives = 10
        Attribute.reset (self)  # Only does a commit here
        
    def commit (self):          # Committing labels is adapting their texts
        self.playerLives_label.text = '{}'.format (self.playerLives)
        self.playerScore_label.text = '{}'.format (self.playerScore)  

class StartScreen (Attribute):
    
    def install (self):
        
        self.pause_text = pyglet.text.Label(
            text='press space to start', 
            font_size=40 , 
            italic=True, 
            bold=True, 
            x=start_Window_width//2 , 
            y=start_Window_height//2-50, 
            anchor_x='center', 
            anchor_y='center', 
            batch=self.game.batch)
        self.instr_text = pyglet.text.Label(
            text='after that: <- -> for moving, space for shooting', 
            font_size=20, 
            italic=True, 
            x=start_Window_width//2, 
            y=start_Window_height//2-100, 
            anchor_x='center', 
            anchor_y='center', 
            batch=self.game.batch)

    def reset (self):
        if not self.game.pause:
            self.gameover_screen.pause_text.delete()
            self.gameover_screen.instr_text.delete()

class GameOverScreen (Attribute):

    def install (self):
        self.game_over_label = pyglet.text.Label(
            text='GAME OVER', 
            font_size=60 , 
            italic=True, 
            bold=True, 
            x=start_Window_width//2 , 
            y=start_Window_height//2-50, 
            anchor_x='center', 
            anchor_y='center', 
            batch=self.game.batch)
        self.play_again_label = pyglet.text.Label(
            text='wanna play again? press space for reset', 
            font_size=20, 
            italic=True, 
            x=start_Window_width//2, 
            y=start_Window_height//2-100, 
            anchor_x='center', 
            anchor_y='center', 
            batch=self.game.batch)

    def reset (self):
        if not self.game.gameover:
            self.gameover_screen.game_over_label.delete()
            self.gameover_screen.play_again_label.delete()





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
        self.gameover = False
        self.player_fire_rate = 0

        self.attributes = []
        
        #self.spaces = [Space (self, index) for index in range (2)]
        #print (self.spaces[0].pos_x, self.spaces[0].pos_y)
        #print (self.spaces[0].pygletSprite.x, self.spaces[0].pygletSprite.y)
        #print (self.spaces[1].pos_x, self.spaces[1].pos_y)
        #print (self.spaces[1].pygletSprite.x, self.spaces[1].pygletSprite.y)
        
        self.start_screen = StartScreen(self)
        #self.gameover_screen = GameOverScreen(self)

        self.player_ship = Player_Ship(self)
        self.enemy_ships = []
        for i in range (5):
            self.enemy_ships.append(Enemy_Ship(self))
        self.scoreboard = Scoreboard (self)

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
        
        
        if self.pause and not self.gameover:  
            self.attributes.append(self.start_screen)                                    # If in paused state
            if self.keymap [pyglet.window.key.SPACE]:       #   If SPACEBAR hit
                self.start_screen.pause_text.delete()
                self.start_screen.instr_text.delete()
                self.pause = False          
                #self.attributes.reset()                #       Start playing
                time.sleep(0.5)
            #elif self.keymap [pyglet.window.key.ENTER]:     #   Else if ENTER hit
            #   self.scoreboard.reset ()                    #       Reset score
            elif self.keymap [pyglet.window.key.ESCAPE]:    #   Else if ESC hit
                self.exit ()                                #       End game
        elif self.pause and self.gameover:
            if self.keymap [pyglet.window.key.SPACE]:
                self.gameover=False
                self.gameover_screen.game_over_label.delete()
                self.gameover_screen.play_again_label.delete()
                #self.attributes.reset()

            

        else:                                               # Else, so if in active state
            for attribute in self.attributes:               #   Compute predicted values
                attribute.predict ()
                
            for attribute in self.attributes:               #   Correct values for bouncing and scoring
                attribute.interact ()
                
            for attribute in self.attributes:               #   Commit them to pyglet for display
                attribute.commit ()


        self.count = 0
        for item in self.attributes:
            if type(item) is Enemy_Ship:
                #gc.collect()
                #print(gc.get_referrers(item))
                self.count += 1
        #print(self.player_ship.player_fire)
        #print(self.attributes.count(Enemy_Ship))

        #print(self.count)  

    def draw (self):
        self.window.clear ()
        self.batch.draw ()      # All attributes added their graphical representation to the batch
    

    def game_over(self):
        self.gameover = True
        self.pause = True
        self.gameover_screen = GameOverScreen(self)
        self.scoreboard.playerLives +=10
        self.scoreboard.playerScore = 0

        '''
        if self.keymap [pyglet.window.key.SPACE]:
            #self.attributes.delete(self.gameover_screen)
            self.gameover_screen.game_over_label.delete()
            self.gameover_screen.play_again_label.delete()
            self.attributes.reset()
        '''
        #print(self.attributes)
        #self.attributes.reset()
        #self.update()



game = Game()





'''
notes:
to do:

- enemy_ships:
    - nu verwijdert ie ook het ship dat er boven zit (laser raakt het nog)
    - spacing beter
- explosies toevoegen (appenden en na tijdperiode weer removen uit attributen?)
- tekst (intro en game over) op voorgrond en eventueel alles erachter weg
- spaces: kijken of het wel zo goed gaat, want 1) index doorgeven bij nieuwe? 2)als je iets uit lijst verwijdert, shuif index ook op?
- resizable window (zie onderaan)
- geluiden toevoegen
- uitzoeken hoe ik in player_ship window kan gebruiken (nu error dat ie niet herkent dat game een window attribute heeft) > nu maar gewoon pixels aangeven


feedback:
- geen deltaT die aangepast wordt ivm processor
- goed dat uitbreidbaar 
'''








