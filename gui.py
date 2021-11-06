from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

class TokenInput(TextInput):
    def build(self):
        self.multiline = False
        self.text = "cryptocurrency"
        self.focus = True
        self.bind(on_text_validation=on_enter)
        self.bind(text=on_text)
    
    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        print(s)
        return super(TokenInput, self).insert_text(s, from_undo=from_undo)

    def on_enter(self, value):
        print('User pressed enter in: ', self)

    def on_text(self, value):
        print('Cryptocurrency selected: ' + value)

class MyApp(App):
    def build(self):
        parent = Widget()
        Window.clearcolor = (255, 255, 255, 0) # background color for the window
        '''tokeninput = TextInput(multiline=False, text='cryptocurrency', focus=True)
        parent.add_widget(tokeninput)
        tokeninput.bind(on_text_validation=on_enter)
        tokeninput.bind(text=on_text)'''
        tokeninput = TokenInput()
        parent.add_widget(tokeninput)
        return parent

MyApp().run()
