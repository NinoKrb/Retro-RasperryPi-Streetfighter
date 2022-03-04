class Attack():
    def __init__(self, name, action_name, damage, knockback=False, delay=0):
        self.name = name
        self.action_name = action_name
        self.damage = damage
        self.knockback = knockback
        self.delay = delay