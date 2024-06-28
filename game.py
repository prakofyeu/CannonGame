import math
from math import sin, cos, atan, sqrt, pi
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from Obstacle import Obstacle
from Laser import Laser
from Bullet import Bullet
import cannon_constants as CONST
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

SCREEN_WIDTH: int = CONST.SCREEN_WIDTH
SCREEN_HEIGHT: int = CONST.SCREEN_HEIGHT
Initial_velocity = CONST.BULLET_MAX_VEL
Frame_rate = 20.0

class AimWidget(Widget):
    def __init__(self, **kwargs):
        super(AimWidget, self).__init__(**kwargs)
        self.size = (CONST.SCREEN_WIDTH / 3, CONST.SCREEN_HEIGHT / 3)
        self.pos_hint = {'x': 0, 'y': 0}

    def on_touch_down(self, touch):
        print(f"Touch on aim_widget")
class Game(Widget):
    ball = ObjectProperty(None)
    ball_released = False
    start = False
    after = False
    obstacles_added = False
    obstacle = ObjectProperty(None)
    obstacles = ListProperty([])
    chosen_weapon = "bullet"
    laserFired = False

    def __init__(self, manager, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.manager = manager
        self.back_btn = Button(
            text="Exit to menu",
            on_press=self.back_btn_callback,
            pos_hint={'center_x': 0.2, 'center_y': 0.2},
            size_hint=(0.2, 0.1)
        )
        self.add_widget(self.back_btn)
    def back_btn_callback(self, *args, **kwargs):
        self.manager.current = 'menu'
    def change_weapon(self, weapon):
        self.chosen_weapon = weapon
        print(f"chosen weapon is {self.chosen_weapon}")

    def bullet_blast(self, target_block):
        pos = target_block.pos
        # print(len(self.obstacles))
        for obs in self.obstacles[:]:
            distance = sqrt((pos[0] - obs.pos[0])**2 + (pos[1] - obs.pos[1])**2)
            # print(obs.id)
            # print(distance)
            # print(CONST.BULLET_RADIUS)
            if distance <= CONST.BULLET_RADIUS:
                # print("deleted")
                self.remove_obstacle(obs)
            # print()
        # print(len(self.obstacles))

    def laserBlast(self):
        for obs in self.obstacles[:]:
            if Obstacle.laserCollision(obs, self.laser):
                self.remove_obstacle(obs)

    def startGame(self):
        self.start = True

    def remove_obstacle(self, obstacle):
        self.remove_widget(obstacle)
        self.obstacles.remove(obstacle)

    def serve_ball(self, ang, coef):
        if self.chosen_weapon == "bullet":
            self.ball_released = True
            self.ball.pos = SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3
            self.ball.velocity = (Initial_velocity * cos(ang) * coef, Initial_velocity * sin(ang) * coef)
        if self.chosen_weapon == "laser":
            self.fireLaser(ang)

    def fireLaser(self, angle):
        if self.laserFired == False:
            self.laser = Laser(pos=(400,300))
            self.laser.rotate(angle*180/pi - 90)
            print(angle)
            self.add_widget(self.laser)
            self.laserFired = True
        else:
            print("WAIT")
    def spawn_ball(self):
        self.ball.pos = CONST.SCREEN_WIDTH / 3, CONST.SCREEN_HEIGHT / 3
        self.ball.velocity = (0, 0)
        self.ball_released = False

    def addObstacles(self, pos, object_id, n_of_obstacles_x, n_of_obstacles_y):
        print("obstacles added")
        for i in range(n_of_obstacles_x):
            for j in range(n_of_obstacles_y):
                obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"))
                self.add_widget(obstacle)
                self.obstacles.append(obstacle)
        self.obstacles_added = True

    def update(self, dt):
        for obstacle in self.obstacles:
            if obstacle.obstacle_collision(self.ball):
                self.bullet_blast(obstacle)
                self.spawn_ball()
                # self.remove_obstacle(obstacle)
            if self.laserFired:
                if obstacle.laserCollision(self.laser):
                    self.laserBlast()
                    print("collision")
        if self.ball_released:
            self.ball.move()
            if self.ball.pos[0] > CONST.SCREEN_WIDTH + 10:
                self.spawn_ball()
        if self.chosen_weapon == "laser" and self.laserFired:
            if self.laser.size[0] > 0:
                self.laser.size[0] -= 2
            else:
                self.remove_widget(self.laser)
                self.laserFired = False

        if self.start:
            print("game started")
            but = self.ids["start_button"]
            self.remove_widget(but)
            self.start = False
            self.after = True

    # def on_touch_down(self, touch):
    #     if self.after:
    #         self.spawn_ball()
    #     else:
    #         Clock.schedule_once(lambda dt: self.on_touch_down(touch))
    #         return super(Game, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if (touch.x < self.width / 3) and (touch.y < self.height / 3):
            angle = atan((self.height / 3 - touch.y) / (self.width / 3 - touch.x))
            c = sqrt(((self.height / 3) - touch.y) ** 2 + (self.width / 3 - touch.x) ** 2) / sqrt(
                ((self.height / 3) ** 2 + (self.width / 3) ** 2))
            self.serve_ball(ang=angle, coef=c)



