from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
import cannon_constants as C
class Laser(Widget):
    angle = NumericProperty(0)
    def __init__(self, pos = None, object_id = 1, **kwargs):
        super().__init__(**kwargs)
        if pos == None:
            pos = 0,0
        self.id = object_id
        self.pos = pos
        self.angle = 0
        self.origin = C.SCREEN_WIDTH/3, C.SCREEN_HEIGHT/3

    def rotate(self, delta_angle):
        self.angle = delta_angle
        print(f"actual angle = {self.angle}")
