class Action():
    def __init__(self, default_action=False):
        self.current_action = { 'name': None, 'loop': False }
        self.clear_queue()
        if default_action != False:
            self.default_action = default_action
            self.next_action = default_action
            self.change_action(default_action)

    def change_action(self, action):
        self.current_action = action
        
    def queue_action(self, name, loop=False):
        self.next_action = { 'name': name, 'loop': loop }

    def clear_queue(self):
        self.next_action = None

    def force_change_action(self, name, loop=False):
        self.queue_action(name, loop)
        self.change_action(self.next_action)
        self.clear_queue()

    def reset_action(self):
        if self.default_action != False:
            self.current_action = self.default_action

    def is_next_action_queued(self):
        if self.current_action != self.next_action:
            return self.next_action

        else:
            False