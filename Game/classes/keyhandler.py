import os,sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

class KeyBind():
    def __init__(self, event, key, type, action, payload=None):
        self.event = event
        self.type = type
        self.action = action
        self.key = key
        self.payload = payload

class KeyHandler():
    def __init__(self, target, keybinds):
        self.keybinds = keybinds
        self.target = target

    def add_keybind(self, keybind):
        self.keybinds.append(keybind)

    def remove_keybind(self, keybind):
        for keybinding in self.keybinds:
            if keybinding == keybind:
                self.keybinds.remove(keybind)

    def activate_keybind(self, key):
        for keybind in self.keybinds:
            if keybind.key == key:
                self.target.handle_keybind(keybind)
