from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label

class HallOfFame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(
            text="Меня ебало три собаки(это холл оф фейм)",
            pos_hint={'center_x': 0.3, 'center_y': 0.3},
            size_hint=(0.2, 0.1)
        )
        self.back_btn = Button(
            text="Back to menu",
            on_press=self.back_btn_callback,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.2, 0.1)
        )
        self.add_widget(self.label)
        self.add_widget(self.back_btn)
    def back_btn_callback(self, *args, **kwargs):
        self.manager.current = "menu"