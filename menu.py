from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle

class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_game_btn = Button(
            text="Play",
            on_press=self.start_game_btn_callback,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.2, 0.1)
        )
        self.help_btn = Button(
            text = "Help",
            on_press = self.help_callback,
            pos_hint={'center.x': 0.1, 'center_y': 0.1},
            size_hint=(0.2, 0.1)
        )
        self.hall_of_fame_btn = Button(
            text = "Hall Of Fame",
            on_press = self.hall_of_fame_callback,
            pos_hint={'center.x': 0.3, 'center_y': 0.3},
            size_hint=(0.2, 0.1)
        )
        self.add_widget(self.start_game_btn)
        self.add_widget(self.help_btn)
        self.add_widget(self.hall_of_fame_btn)
        with self.canvas.before:
            self.rect = Rectangle(pos=(self.x, self.y), size=(1000, 900), source='startbg.jpg')
    def start_game_btn_callback(self, *args, **kwargs):
        self.manager.current = 'game'
    def help_callback(self, *args, **kwargs):
        self.manager.current = 'help'
    def hall_of_fame_callback(self, *args, **kwargs):
        self.manager.current = 'hall_of_fame'