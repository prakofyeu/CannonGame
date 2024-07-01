from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import (
    NumericProperty, ReferenceListProperty
)
from kivy.graphics import Ellipse
from cannon_constants import BOMB_MASS, BOMB_DRILL, BOMB_MAX_VEL
Frame_rate = 20.0
Free_fall_acceleration = 9.81


class Bomb(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    drill = BOMB_DRILL
    def __init__(self, **kwargs):
        super(Bomb, self).__init__(**kwargs)
        
        
        with self.canvas:
            self.rect = Ellipse(pos=(self.x, self.y), size=(20, 20), source='bomb.png')

    def move(self):
        self.velocity = self.velocity_x, self.velocity_y - (Free_fall_acceleration / Frame_rate)
        self.pos = Vector(*self.velocity) + self.pos