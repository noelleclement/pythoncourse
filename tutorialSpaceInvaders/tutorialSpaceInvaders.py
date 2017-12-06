import pyglet
from pyglet.window import key, FPSDisplay
import numpy as np

def preload_image(image):
    img = pyglet.image.load('resources/sprites/'+image)
    return img

  

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(150,50)
        self.frame_rate = 1/60.0      
        #self.fps_display = FPSDisplay(self)   
        #self.fps_display.label.font_size = 50     

        #self.main_batch = pyglet.graphics.Batch()

        self.right = False
        self.left = False
        self.player_speed = 300  
        #self.fire = False   
        #self.player_fire_rate = 0                     

        self.player_img = preload_image('PlayerShip.png')
        self.player_spr = pyglet.sprite.Sprite(self.player_img)
        self.player = GameAttribute(500, 100, 0, 0, self.player_spr)             #why can you put the image as a later parameter (otherwise it gives an error)
        
        '''
        self.player_laser_list = []                         #niet zo'n goede datastructuur? is wel redelijk opgelost met if statement bij update_player_laser
        self.player_laser_img = preload_image('laser.png')
        self.player_laser_sprite = pyglet.sprite.Sprite(self.player_laser_img)
        self.player_laser = GameAttribute(self.player.pos_x+(self.player.width/2.0-(self.player_laser_img.width/2.0)), self.player.pos_y+self.player.height, 0, 0, self.player_laser_sprite)
        '''

        #rest van player_laser_list staat in def player_fire

        self.space_img = preload_image('space.jpg')
        self.space_list = []
        self.space_sprite = pyglet.sprite.Sprite(self.space_img)
        

        #initiate scrolling background
        for spc in range(2):
            self.space_list.append(GameAttribute(0, spc*1200, 0, -100, self.space_sprite))

        '''   
        self.enemy_ship = preload_image('enemyShip_Sh01.png')
        self.enemy_ship_seq = pyglet.image.ImageGrid(self.enemy_ship, 1, 15, item_width=100, item_height=100)
        self.enemy_ship_anim = pyglet.image.Animation.from_image_sequence(self.enemy_ship_seq[0:], 0.1, loop=True)
        
        self.enemy_ship_sprite = pyglet.sprite.Sprite(self.enemy_ship_anim, np.random.randint(200,600), np.random.randint(500,800), batch=self.main_batch)
        self.enemy_ship_list = []
        for enship in range(5):               #miss variabele met hoeveel enemies
            self.enemy_ship_list.append(self.enemy_ship_sprite)
        '''
    
    

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = True
        if symbol == key.LEFT:
            self.left = True
        #if symbol == key.SPACE:
        #    self.fire = True
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:                 #hoe kan dit, waarom moet het niet != key.Right zijn? (geldt ook voor left)
            self.right = False
        if symbol == key.LEFT:
            self.left = False
        #if symbol == key.SPACE:
        #    self.fire = False


    def on_draw(self):
        self.clear()
        for spc in self.space_list:
            spc.draw()
        self.player.draw()                                   #later make an encompassing class with all sprites?
        #for lsr in self.player_laser_list:
        #   lsr.draw()
        #self.main_batch.draw()
        #self.fps_display.draw()

    def update_player(self, dt):
        self.player.update(dt)
        if self.right and self.player.pos_x < 1000 - self.player.width:                 #hier integreren grootte beeldscherm (hij stopt nu 200 pixels vd rechterkant, relatief tot linkerkant afbeelding)
            self.player.pos_x += self.player_speed * dt
        if self.left and self.player.pos_x > 100:                    #hier integreren grootte beeldscherm + grootte afbeelding (hij stopt nu 100 pixels vd linkerkant, relatief tot linkerkant afbeelding)
            self.player.pos_x -= self.player_speed * dt

    '''
    def update_player_laser(self, dt):
        for lsr in self.player_laser_list:
            lsr.update(dt)
            lsr.pos_y += 400 * dt
            if lsr.pos_y > 900:                                     #hier iets toevoegen van beeldschermgrootte
                self.player_laser_list.remove(lsr)      
    
    def player_fire(self, dt):
        self.player_fire_rate -= dt
        if self.player_fire_rate <= 0:
            self.player_laser_list.append(self.player_laser)
            self.player_fire_rate += 0.2                                # waarom precies 0.2? kan dit relatief tot iets zijn?
    '''
    
    def update_space(self,dt):
        for spc in self.space_list:
            spc.update(dt)
            if spc.pos_y <= -1300:                                  #windowsize add
                self.space_list.remove(spc)                                                     #if bottom image is below screen, remove and create new image and add to list (see below)
                self.space_list.append(GameAttribute(0, 1100, 0, -100, self.space_sprite))             #is this an elegant way to solve the scrolling (creating new background), is the list just growing?
    

    def update(self, dt):
        self.update_player(dt)
        #if self.fire:
        #    self.player_fire(dt)
        #self.update_player_laser(dt)
        self.update_space(dt)
       


class GameAttribute:
    def __init__(self, pos_x, pos_y, vel_x, vel_y, sprite=None):            #ik snap nog niet helemaal waarom de sprite sprite heet (heette eerst image, maar is nu een apart functie voor refactoring)
        self.pos_x = pos_x                      #start position xcoor based on given parameter
        self.pos_y = pos_y                      #start position xcoor based on given parameter
        self.vel_x = vel_x                           #velocity x
        self.vel_y = vel_y                           #velocity y
        
        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.pos_x
            self.sprite.y = self.pos_y
            self.width = self.sprite.width
            self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def update(self, dt):                       #dt = deltatime
        self.pos_x += self.vel_x*dt
        self.pos_y += self.vel_y*dt
        self.sprite.x = self.pos_x
        self.sprite.y = self.pos_y



if __name__ == "__main__":
    window = GameWindow(1200, 800, "Space Invaders", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)      
    pyglet.app.run()



"""
to do:
- window relatief tot beeldscherm maken (full screen of x-*iets* etc) (let op background, die is y1200 > lijkt niet uit te maken want heeft meer te maken met image)
- ik heb nu sprite functies in het algemene gameattribute staan, dit is niet de bedoeling
- framerate meer realtime (zie assignment) 
- alles door pushen (in algemene attributes een update, maar ook in elke attribute zelf? en dan link je die allemaal en dan hoef je in update alleen maar die ene attribute aan te roepen?)
- player als onderdeel van een grotere groep sprites
- space aparte attribute 
- naam: geen window, maar wat je ziet
- niet van window erven ( proberen niet te veel afhankelijk van pyglet.window.Window, let op uitbreidbaarheid + vernieuwbaarheid, maar alleen als nog tijd over)
- centrale key handler
- kijken of def preload_image op een betere plek kan (en als binnen een classe, dan nog bruikbaar erbuiten?)
- kijken of bepaalde variabelen centraal bepaald kunnen worden (makkelijk aan te passen)
- misschien kan ik de velocity meegeven met de update (dus in gameattribute in de update wordt de velocity dan meegerekend) > doet ie nu al maar dat kan voor player bijv handiger zijn want nu wordt dat allemaal in update player gedaan

"""