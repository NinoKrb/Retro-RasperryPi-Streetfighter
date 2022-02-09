class AnimationSet():
    def __init__(self, name, animations):
        self.name = name
        self.animations = animations
        self.animation_set = self.get()

        self.current_animation = { 'name': '', 'current_frame': 0, 'frames': [] }
        self.default_animation = None

    def get(self):
        animation_set = { 'name': '', 'animations': [], 'amount': 0 }
        animation_set['name'] = self.name

        for animation in self.animations:
            animation_set['animations'].append({ 'name': animation.animation_name, 'frames': animation.animation_frames, 'duration': animation.animation_delay })
        
        animation_set['amount'] = len(self.animations)
        return animation_set

    def get_animation(self, name):
        for animation in self.animation_set['animations']:
            if animation['name'] == name:
                return animation

    def change_current_animation(self, animation_name):
        self.current_animation['name'] = animation_name
        self.current_animation['frames'] = self.get_animation(animation_name)['frames']
        self.current_animation['current_frame'] = 0
        self.current_animation['duration'] = self.get_animation(animation_name)['duration']

    def play_animation(self):
        if len(self.current_animation['frames']) > 0:
            if self.current_animation['duration'].is_next_stop_reached():
                self.current_animation['current_frame'] += 1

                if len(self.current_animation['frames']) <= self.current_animation['current_frame']:
                    self.current_animation['current_frame'] = 0

                return self.current_animation['frames'][self.current_animation['current_frame']]
            else:
                return False
        else:
            return False


