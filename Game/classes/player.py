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
    def __init__(self, id, health, size, pos, flip, player_images, animations, attacks, speed, colorkey):
        super().__init__()

        # Essential
        self.id = id

        # Default Values
        self.default_fallback_image = player_images['fallback']
        self.default_avatar_image = player_images['avatar']
        self.default_size = size
        self.default_colorkey = colorkey
        self.default_speed = speed
        self.default_pos = { 'x': pos[0], 'y': pos[1] }
        print('Init',self.default_pos)
        self.default_flip = flip
        self.default_health = health
        self.default_max_health = health
        self.default_attacks = attacks
        self.default_animation_set = self.load_animation_set(animations)
        
        # Reset Player Values
        self.reset()

    def reset(self):
        # Sprite
        self.fallback_image = self.default_fallback_image
        self.avatar_image = self.default_avatar_image
        self.size = self.default_size
        self.colorkey = self.default_colorkey
        
        # Movement
        self.speed = self.default_speed
        self.pos = self.default_pos
        self.direction = None
        self.flip = self.default_flip
        self.freeze = False

        # Gravity
        self.is_jumping = False
        self.player_y_momentum = 0

        self.moving = {'right': False, 'left': False}
        self.jumps_left = 2

        # Fight
        self.health = self.default_health
        self.max_health = self.default_health
        self.attacks = self.default_attacks
        self.current_attack = None
        self.is_attacking = False
        
        # Animation & Actions
        self.animation_set = self.default_animation_set
        self.action_manager = Action({ 'name': 'idle', 'loop': False })
        self.animation_set.change_current_animation(self.action_manager.current_action['name'])
        self.update_sprite(os.path.join('players', f'player_{self.id}', self.fallback_image))

        self.set_pos(self.default_pos['x'], self.default_pos['y'])
        
    def load_animation_set(self, animations):
        animation_objects = []
        for animation in animations:
            animation_objects.append(Animation(animation['name'], os.path.join('players', f'player_{self.id}', 'animations', animation['name']), animation['duration']),)

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
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.image.set_colorkey(self.colorkey)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.set_pos(self.pos['x'], self.pos['y'])

    def update(self, game):
        self.game = game
        self.process_animation()
        if not self.freeze:
            self.move_velocity()
            self.gravity()
        self.set_coords()
        self.check_fight_collision()

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
            frame = os.path.join('players', f'player_{self.id}', 'animations', self.animation_set.current_animation['name'], frame)
            self.update_sprite(frame)
            if self.animation_set.current_animation['current_frame'] == 0:
                next_action = self.action_manager.is_next_action_queued()
                if self.is_attacking:
                    self.is_attacking = False
                    self.freeze = False

                if next_action:
                    self.action_manager.change_action(next_action)
                    self.animation_set.change_current_animation(next_action['name'])

                elif self.action_manager.current_action['loop'] == False:
                    self.action_manager.reset_action()
                    self.animation_set.change_current_animation(self.action_manager.current_action['name'])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handle_movement(self, payload):
        if not self.moving[str(payload['direction'])]:
            self.change_direction(payload['direction'])
            self.flip = payload['flip']

            self.move_direction()
            self.action_manager.force_change_action(payload['animation'], payload['loop'])
            self.animation_set.change_current_animation(self.action_manager.current_action['name'])
        else:
            print("Already Moving")

    def stop_handle_movement(self, payload):
        self.stop_move_direction(payload['direction'])

        if not self.moving['left'] and not self.moving['right']:
            if not self.is_jumping:
                self.action_manager.reset_action()
                self.action_manager.clear_queue()

            if self.is_attacking:
                self.is_attacking = False
                self.freeze = False


        if self.moving['left']:
            self.flip = True

        else:
            self.flip = False

    def handle_attack(self, payload):
        if not self.is_attacking:
            self.current_attack = self.find_attack(payload['animation'])
            self.action_manager.force_change_action(payload['animation'], payload['loop'])
            self.animation_set.change_current_animation(self.action_manager.current_action['name'])
            self.is_attacking = True

    def find_attack(self, action_name):
        for attack in self.attacks:
            if attack.action_name == action_name:
                return attack

    def check_fight_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.players, False, pygame.sprite.collide_circle_ratio(Settings.player_collide_ratio))
        for hit in hits:
            if hit != self and hit.is_attacking:
                self.handle_hit(hit, hit.current_attack)

    def handle_hit(self, attacker, attack):
        self.freeze = True
        self.health -= attack.damage
        if attack.knockback:
            if attacker.rect.center < self.rect.center:
                self.rect.move_ip(attack.knockback * 2, -attack.knockback * 4)
            else:
                self.rect.move_ip(-attack.knockback * 2, -attack.knockback * 4)
        self.freeze = False