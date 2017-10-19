
import pyglet




"""
@window.event
def on_mouse_press(x, y, button, modifiers):
    print('press')

@window.event
def on_mouse_release(x, y, button, modifiers):
    print('release\n')
"""

class Field():

    def __init__(self):
        self.window = pyglet.window.Window()
        self.label = pyglet.text.Label('Hello, world',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=self.window.width//2, y=self.window.height//2,
                                  anchor_x='center', anchor_y='center')
        self.draw()

   
    def draw(self):
        self.window.clear()
        self.label.draw()


class Game():

    def __init__(self):
        self.field = Field()




game = Game()
pyglet.app.run()
