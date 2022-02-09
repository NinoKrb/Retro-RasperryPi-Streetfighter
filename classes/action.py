class Action():
    def __init__(self, default_action=False):
        self.current_action = { 'name': None, 'loop': False }
        if default_action != False:
            self.default_action = default_action
            self.change_action(default_action)

    def change_action(self, action):
        self.current_action = action
        
    def queue_action(self, name, loop=False):
        self.next_action = { 'name': name, 'loop': loop }