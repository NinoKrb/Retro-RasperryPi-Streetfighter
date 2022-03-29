import os,sys
from gpiozero import Button

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings

class ControllerBind():
    def __init__(self, pin, type, action, payload=None):
        self.type = type
        self.action = action
        self.pin = pin
        self.payload = payload
        self.pressed = False
        self.button = Button(self.pin, pull_up = True)

class ControllerHandler():
    def __init__(self, target, keybinds):
        self.keybinds = keybinds
        self.target = target

    def add_keybind(self, keybind):
        self.keybinds.append(keybind)

    def remove_keybind(self, keybind):
        for keybinding in self.keybinds:
            if keybinding == keybind:
                self.keybinds.remove(keybind)
