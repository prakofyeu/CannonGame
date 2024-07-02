from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.graphics import Rectangle

class Help(Screen):
    helpText = """
    The goal of the game is to get as much score as possible
    On each level you have different amount of shots, so be careful
    Click on the left bottom part of the screen to launch a projectile
    You can switch types of projectiles by clicking the buttons in the upper left corner
    In the hall of fame you can see the best scores
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(
            text=self.helpText,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.2, 0.1),
            font_size = "20dp",
            color =  (1, 1, 0, 1)
        )
        self.back_btn = Button(
            text="Back to menu",
            on_press=self.back_btn_callback,
            pos_hint={'center_x': 0.1, 'center_y': 0.1},
            size_hint=(0.2, 0.1)
        )
        self.add_widget(self.label)
        self.add_widget(self.back_btn)
        with self.canvas.before:
            self.rect = Rectangle(pos=(self.x, self.y), size=(1000, 900), source='helpbg.jpg')
    def back_btn_callback(self, *args, **kwargs):
        self.manager.current = "menu"