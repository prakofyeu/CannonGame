from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from menu import Menu
from game import Game
from cannon_constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from help import Help
from hall_of_fame import HallOfFame

Config.set('graphics', 'width', SCREEN_WIDTH)
Config.set('graphics', 'height', SCREEN_HEIGHT)
Config.set('graphics', 'maxfps', FPS)

class CannonGameScreen(Screen):
     def __init__(self, manager, **kwargs):
        super(CannonGameScreen, self).__init__(**kwargs)
        game = Game(manager=manager)
        self.add_widget(game)
        Clock.schedule_interval(game.update, 1.0 / FPS)

class CannonApp(App):
    def build(self):
        screen_manager = ScreenManager()
        game = CannonGameScreen(name='game', manager=screen_manager)
        
        screen_manager.add_widget(Menu(name='menu'))
        screen_manager.add_widget(game)
        screen_manager.add_widget(Help(name='help'))
        screen_manager.add_widget(HallOfFame(name='hall_of_fame'))
        return screen_manager
    
if __name__ == '__main__':
    CannonApp().run()