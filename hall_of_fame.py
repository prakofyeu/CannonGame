from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.graphics import Rectangle

class HallOfFame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file = open("best_score.txt", "r")
        best_score = file.read()
        file.close()
        self.record_text = "The best score is " + best_score
        self.label = Label(
            text=self.record_text,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.2, 0.1),
            font_size = "40dp"
        )
        self.back_btn = Button(
            text="Back to menu",
            on_press=self.back_btn_callback,
            pos_hint={'center_x': 0.1, 'center_y': 0.1},
            size_hint=(0.2, 0.1)
        )
        self.update_btn = Button(
            text="Update best score",
            on_press=self.update_btn_callback,
            pos_hint={'center_x': 0.3, 'center_y': 0.1},
            size_hint=(0.2, 0.1)
        )
        self.add_widget(self.label)
        self.add_widget(self.back_btn)
        self.add_widget(self.update_btn)
        with self.canvas.before:
            self.rect = Rectangle(pos=(self.x, self.y), size=(1000, 900), source='hfbg.jpg')
    def back_btn_callback(self, *args, **kwargs):
        self.manager.current = "menu"
    def update_btn_callback(self, *args, **kwargs):
        file = open("best_score.txt", "r")
        best_score = file.read()
        file.close()
        self.record_text = "The best score is " + best_score
        self.label.text = self.record_text