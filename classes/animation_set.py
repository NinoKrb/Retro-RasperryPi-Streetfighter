class AnimationSet():
    def __init__(self, name, animations):
        self.name = name
        self.animations = animations

    def get(self):
        animation_set = { 'name': '', 'animations': [], 'amount': 0 }
        animation_set['name'] = self.name

        for animation in self.animations:
            animation_set['animations'].append({ 'name': animation.animation_name, 'frames': animation.animation_frames })

        animation_set['amount'] = len(self.animations)
        return animation_set