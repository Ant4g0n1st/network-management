from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.graphics import Color

from kivy.app import App

from threading import Thread
import time

class TreeViewButton(Button, TreeViewNode):

    def __init__(self, text, fontSize = 14):
        TreeViewNode.__init__(self)
        Button.__init__(self)
        self.text = text

class LoginScreen(BoxLayout):

    def __init__(self):
        BoxLayout.__init__(self)
        self.orientation = 'horizontal'
        self.add_widget(AsyncImage(source = 'mvc.png', size_hint = (0.3, 1), allow_stretch = True))
        self.add_widget(AsyncImage(source = 'mvc.png', size_hint = (0.7, 1), allow_stretch = True))

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
