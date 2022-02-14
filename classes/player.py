from operator import ne
import os,sys,pygame

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings
from classes.animation_set import AnimationSet
from classes.animation import Animation
from classes.action import Action

class Player(pygame.sprite.Sprite):
    def __init__(self, id, size, pos, fallback_image, animations, speed, colorkey):
        super().__init__()

        # Essential
        self.id = id

        # Sprite
        self.fallback_image = fallback_image
        self.size = size
        self.colorkey = colorkey

        # Movement
        self.speed = speed
        self.pos = { 'x': pos[0], 'y': pos[1] }
        self.direction = None
        self.flip = False

        # Gravity
        self.is_jumping = False
        self.player_y_momentum = 0

        self.moving = {'right': False, 'left': False}
        self.jumps_left = 2

        # Animation & Actions
        self.animation_set = self.load_animation_set(animations)
        self.action_manager = Action({ 'name': 'idle', 'loop': False })
        self.animation_set.change_current_animation(self.action_manager.current_action['name'])
        self.update_sprite(os.path.join('players', 'player_1', self.fallback_image))

    def load_animation_set(self, animations):
        animation_objects = []
        for animation in animations:
            animation_objects.append(Animation(animation['name'], os.path.join('players', 'player_1', 'animations', animation['name']), animation['duration']),)

        return AnimationSet('Player', animation_objects) 

    def change_direction(self, direction):
        self.direction = direction

    def set_pos(self, x, y):
        self.rect.top = y
        self.rect.left = x

    def set_coords(self):
        self.pos['x'] = self.rect.left
        self.pos['y'] = self.rect.top

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.flip, False)
        self.image.set_colorkey(self.colorkey)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.set_pos(self.pos['x'], self.pos['y'])

    def update(self, game):
        self.game = game
        self.process_animation()
        self.move_velocity()
        self.gravity()
        self.set_coords()

    def gravity(self):
        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += Settings.player_y_momentum

        if self.player_y_momentum > Settings.player_max_y_momentum:
            self.player_y_momentum = Settings.player_max_y_momentum

        self.collisions = self.move([self.game.arena.floor])
        if self.collisions['bottom']:
            self.jumps_left = 2
            if self.is_jumping:
                self.action_manager.queue_action('run', True)
            self.is_jumping = False
            self.jump_velocity = 0
            self.player_y_momentum = 0

    def move(self, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.player_movement[0]
        self.rect.y += self.player_movement[1]

        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)

        for tile in hit_list:
            if self.player_movement[1] > 0:
                self.rect.bottom = tile.rect.top
                collision_types['bottom'] = True

        return collision_types

    def jump(self, force=False):
        if self.is_jumping == False or self.jumps_left > 0 or force == True:
            self.is_jumping = True
            self.player_y_momentum = Settings.player_jump_height
            self.jumps_left -= 1
            self.action_manager.force_change_action('jump', False)
            self.animation_set.change_current_animation(self.action_manager.current_action['name'])

    def move_velocity(self):
        self.player_movement = [0, 0]

        if self.moving['right']:
            self.player_movement[0] += Settings.player_speed
            if self.is_jumping == False:
                self.is_walking = True
        if self.moving['left']:
            self.player_movement[0] -= Settings.player_speed
            if self.is_jumping == False:
                self.is_walking = True

    def move_direction(self):
        if self.direction == "left":
            self.moving['left'] = True
        elif self.direction == "right":
            self.moving['right'] = True

    def stop_move_direction(self, direction):
        if direction == "left":
            self.moving['left'] = False
        elif direction == "right":
            self.moving['right'] = False

    def process_animation(self):
        frame = self.animation_set.play_animation()
        if frame:
            frame = os.path.join('players', 'player_1', 'animations', self.animation_set.current_animation['name'], frame)
            self.update_sprite(frame)
            if self.animation_set.current_animation['current_frame'] == 0:
                next_action = self.action_manager.is_next_action_queued()
                if next_action:
                    self.action_manager.change_action(next_action)
                    self.animation_set.change_current_animation(next_action['name'])

                elif self.action_manager.current_action['loop'] == False:
                    self.action_manager.reset_action()
                    self.animation_set.change_current_animation(self.action_manager.current_action['name'])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handle_movement(self, payload):
        self.change_direction(payload['direction'])
        self.flip = payload['flip']

        self.move_direction()
        self.action_manager.force_change_action(payload['animation'], payload['loop'])
        self.animation_set.change_current_animation(self.action_manager.current_action['name'])

    def stop_handle_movement(self, payload):
        self.stop_move_direction(payload['direction'])

        if not self.is_jumping:
            self.action_manager.reset_action()
            self.action_manager.clear_queue()
        self.animation_set.change_current_animation(self.action_manager.current_action['name'])

    def handle_attack(self, payload):
        self.action_manager.force_change_action(payload['animation'], payload['loop'])
        self.animation_set.change_current_animation(self.action_manager.current_action['name'])