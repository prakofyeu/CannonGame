from kivy.uix.widget import Widget
from kivy.graphics import Rectangle




class Obstacle(Widget):
    def __init__(self, pos = None, object_id = 1, type = "rock", **kwargs):
        super().__init__(**kwargs)
        if pos == None:
            pos = 0,0
        self.id = object_id
        self.pos = pos
        self.size = 30, 30
        self.type = type
        with self.canvas:
            if self.type == "rock":
                self.rect = Rectangle(pos=(self.x, self.y), size=(30, 30), source='rock.png')
            elif self.type == "perpetio":
                self.rect = Rectangle(pos=(self.x, self.y), size=(30, 30), source='perpetio.png')
            elif self.type == "mirror":
                self.rect = Rectangle(pos=(self.x, self.y), size=(30, 30), source='mirror.png')
    def obstacle_collision(self, ball):
        if self.collide_widget(ball):
            return True
    # def laserCollision(self, laser):
    #     if self.collide_widget(laser):
    #         return True
    def laserCollision(self, pointx, pointy):
        self.linearOffset = 5
        self.diagonalOffset = 5
        if self.collide_point(pointx, pointy) or self.collide_point(pointx + 5, pointy) or self.collide_point(pointx - 5, pointy) or self.collide_point(pointx, pointy - 5) or self.collide_point(pointx, pointy + 5):
            return True
        elif self.collide_point(pointx - self.diagonalOffset, pointy - self.diagonalOffset) or self.collide_point(pointx + self.diagonalOffset, pointy - self.diagonalOffset) or self.collide_point(pointx + self.diagonalOffset, pointy + self.diagonalOffset) or self.collide_point(pointx - self.diagonalOffset, pointy + self.diagonalOffset):
            return True