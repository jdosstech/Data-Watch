from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class TokenInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        print(s)
        return super(TokenInput, self).insert_text(s, from_undo=from_undo)

    '''
    def on_text(self, value, from_undo=False):
        print('Cryptocurrency selected: ' + str(value))
    '''

    def on_enter(self, value):
        print('Cryptocurrency selected: ' + str(value))

class SelectionScreen(Screen):
    pass

class DataWatchApp(App):
    def build(self):
        screen_manager = ScreenManager()
        selection_screen = SelectionScreen()
        screen_manager.add_widget(selection_screen)
        Window.clearcolor = (255, 255, 255, 0) # background color for the window

        return screen_manager

DataWatchApp().run()
