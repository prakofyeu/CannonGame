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
from kivy.uix.label import Label
from kivy.properties import StringProperty
import random

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
    score = 0
    shots = 0
    ball = ObjectProperty(None)
    ball_released = False
    obstacles_added = False
    obstacle = ObjectProperty(None)
    obstacles = ListProperty([])
    chosen_weapon = "bullet"
    laserFired = False

    def __init__(self, manager, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.manager = manager
        self.back_btn = Button(
            text="Exit game",
            on_press=self.back_btn_callback,
            pos_hint={'center_x': 0.2, 'center_y': 0.2},
            size_hint=(0.2, 0.1)
        )
        self.score_label = Label(
            text = "Current score: " + str(self.score),
            center_x = 100,
            center_y = SCREEN_HEIGHT - 60
        )
        self.game_over_label = Label(
            text = "",
            center_x = SCREEN_WIDTH/2 - 100,
            center_y = SCREEN_HEIGHT/2
        )
        self.start_easy_btn = Button(
            text="Easy level",
            on_press=self.start_easy_btn_callback,
            center_x = 100,
            center_y = SCREEN_HEIGHT - 200,
            size_hint=(0.2, 0.1)
        )
        self.start_medium_btn = Button(
            text="Medium level",
            on_press=self.start_medium_btn_callback,
            center_x = 100,
            center_y = SCREEN_HEIGHT - 300,
            size_hint=(0.2, 0.1)
        )
        self.start_hard_btn = Button(
            text="Hard level",
            on_press=self.start_hard_btn_callback,
            center_x = 100,
            center_y = SCREEN_HEIGHT - 400,
            size_hint=(0.2, 0.1)
        )
        self.shots = 5
        self.add_widget(self.score_label)
        self.add_widget(self.game_over_label)
        self.add_widget(self.back_btn)
        self.add_widget(self.start_easy_btn)
        self.add_widget(self.start_medium_btn)
        self.add_widget(self.start_hard_btn)
    def clear_field(self):
        while len(self.obstacles) != 0:
            for obstacle in self.obstacles:
                if obstacle:
                    self.remove_widget(obstacle)
                    self.obstacles.remove(obstacle)
    
    def start_easy_btn_callback(self, *args, **kwargs):
        self.clear_field()
        self.shots = 10
        self.addObstacles(pos = (800, 500), object_id = 1, n_of_obstacles_x = 10, n_of_obstacles_y = 30, difficulty="easy")
        self.score = 0
        self.score_label.text = "Current score: " + str(self.score)
        self.game_over_label.text = ""
        
    def start_medium_btn_callback(self, *args, **kwargs):
        self.clear_field()
        self.shots = 5
        self.addObstacles(pos = (800, 500), object_id = 1, n_of_obstacles_x = 20, n_of_obstacles_y = 40, difficulty="medium")
        self.score = 0
        self.score_label.text = "Current score: " + str(self.score)
        self.game_over_label.text = ""
        
    def start_hard_btn_callback(self, *args, **kwargs):
        self.clear_field()
        self.shots = 5
        self.addObstacles(pos = (800, 500), object_id = 1, n_of_obstacles_x = 30, n_of_obstacles_y = 40, difficulty="hard")
        self.score = 0
        self.score_label.text = "Current score: " + str(self.score)
        self.game_over_label.text = ""
    
    def back_btn_callback(self, *args, **kwargs):
        self.clear_field()
        self.set_best_score(self.score)
        self.manager.current = 'menu'
    
    def set_best_score(self, score):
        file = open("best_score.txt", "r")
        best_score = int(file.read())
        file.close()
        if score > best_score:
            best_score = score
            file = open("best_score.txt", "w")
            file.write(str(score))
            file.close()
            
    def change_weapon(self, weapon):
        self.chosen_weapon = weapon
        print(f"chosen weapon is {self.chosen_weapon}")

    def bullet_blast(self, target_block):
        pos = target_block.pos
        for obs in self.obstacles[:]:
            distance = sqrt((pos[0] - obs.pos[0])**2 + (pos[1] - obs.pos[1])**2)
            if distance <= CONST.BULLET_RADIUS and obs.type == "rock":
                self.remove_obstacle(obs)

    def laserBlast(self):
        for obs in self.obstacles[:]:
            if Obstacle.laserCollision(obs, self.laser):
                self.remove_obstacle(obs)

    def remove_obstacle(self, obstacle):
        self.remove_widget(obstacle)
        self.obstacles.remove(obstacle)
        self.score += 1
        self.score_label.text = "Current score: " + str(self.score)
        print(self.score)

    def serve_ball(self, ang, coef):
        if self.chosen_weapon == "bullet" and self.shots > 0:
            self.shots -= 1
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

    def addObstacles(self, pos, object_id, n_of_obstacles_x, n_of_obstacles_y, difficulty = "easy"):
        if difficulty == "easy":
            t = 0
            for i in range(n_of_obstacles_x):
             for j in range(n_of_obstacles_y):
                if j%3 == 0:
                    t = random.randint(1,2)
                    if t == 1:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="perpetio")
                    else:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="rock")
                else:
                    obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"))
                self.add_widget(obstacle)
                self.obstacles.append(obstacle)
        elif difficulty == "medium":
            t = 0
            for i in range(n_of_obstacles_x):
             for j in range(n_of_obstacles_y):
                if j%3 == 0:
                    t = random.randint(1,3)
                    if t == 1:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="perpetio")
                    elif t == 2:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="mirror")
                    else:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="rock")
                else:
                    obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"))
                self.add_widget(obstacle)
                self.obstacles.append(obstacle)
        elif difficulty == "hard":
            t = 0
            for i in range(n_of_obstacles_x):
             for j in range(n_of_obstacles_y):
                if j%1 == 0:
                    t = random.randint(1,3)
                    if t == 1:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="perpetio")
                    elif t == 2:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="mirror")
                    else:
                        obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"), type="rock")
                else:
                    obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"))
                self.add_widget(obstacle)
                self.obstacles.append(obstacle)
        self.obstacles_added = True

    def update(self, dt):
        for obstacle in self.obstacles:
            if obstacle.obstacle_collision(self.ball) and obstacle.type == "rock":
                self.bullet_blast(obstacle)
                self.spawn_ball()
            if obstacle.obstacle_collision(self.ball) and (obstacle.type == "perpetio" or obstacle.type == "mirror"):
                self.ball.velocity[0] = -self.ball.velocity[0]
                self.ball.velocity[1] = -self.ball.velocity[1]
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
        if self.shots == 0:
            self.game_over_label.text = "You are out of shots, game over. You score:  " + str(self.score) + "\n" + "Visit hall of fame to see the best result"
                
    def on_touch_up(self, touch):
        if (touch.x < self.width / 3) and (touch.y < self.height / 3):
            angle = atan((self.height / 3 - touch.y) / (self.width / 3 - touch.x))
            c = sqrt(((self.height / 3) - touch.y) ** 2 + (self.width / 3 - touch.x) ** 2) / sqrt(
                ((self.height / 3) ** 2 + (self.width / 3) ** 2))
            self.serve_ball(ang=angle, coef=c)