import math

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Line
import cannon_constants as C
class Laser(Widget):
    angle = NumericProperty(0)
    def __init__(self, object_id = 1, **kwargs):
        super().__init__(**kwargs)
        self.id = object_id
        self.initial_point_x = C.SCREEN_WIDTH/3
        self.initial_point_y = C.SCREEN_HEIGHT/3
        self.fire_time = 0
        self.laser_segments = []
        self.isFired = False
        self.firingLaser = False
        self.angleLaser = 0
        self.width = 10
        self.x = self.initial_point_x
        self.y = self.initial_point_y
        self.Hcol = False
        self.Vcol = False
        self.timeWithoutDestroyingObstacles = 0

    def reset_laser(self):
        self.isFired = False
        self.firingLaser = False
        self.initial_point_x = C.SCREEN_WIDTH/3
        self.initial_point_y = C.SCREEN_HEIGHT/3
        self.x = self.initial_point_x
        self.y = self.initial_point_y
        self.fire_time = 0
        self.Hcol = False
        self.Vcol = False

    def draw_laser_segment(self, delta_angle):
        self.fire_time += 0.1
        self.timeWithoutDestroyingObstacles += 0.1
        if self.Vcol and self.Hcol:
            self.fireCos = math.cos(delta_angle) * -1
            self.fireSin = math.sin(delta_angle) * -1
        elif self.Vcol:
            self.fireCos = math.cos(delta_angle) * -1
            self.fireSin = math.sin(delta_angle) * 1
        elif self.Hcol:
            self.fireCos = math.cos(delta_angle) * 1
            self.fireSin = math.sin(delta_angle) * -1
        else:
            self.fireCos = math.cos(delta_angle) * 1
            self.fireSin = math.sin(delta_angle) * 1


        self.segmentLength = 10
        self.x += self.fireCos * self.segmentLength
        self.y += self.fireSin * self.segmentLength

    def laserReflection(self, type = "horizontal"):
        print(type)
        self.initial_point_x = self.x
        self.initial_point_y = self.y
        if type == "horizontal":
            self.Hcol = not self.Hcol
        if type == "vertical":
            self.Vcol = not self.Vcol
