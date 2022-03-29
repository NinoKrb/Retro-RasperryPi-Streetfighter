import pygame, os, random
from settings import Settings
from classes.player import Player
from classes.keyhandler import KeyHandler, KeyBind
from classes.controllerhandler import ControllerHandler, ControllerBind
from classes.arena import Arena
from classes.attack import Attack
from classes.overlay import Overlay
from helpers.timer import Timer

class Game():
    def __init__(self):
        super().__init__()

        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(Settings.title)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.fps = pygame.time.Clock()

        actions_1 = [
            { 'name': 'idle', 'duration': 100 }, 
            { 'name': 'run', 'duration': 100 }, 
            { 'name': 'jump', 'duration': 75 }, 
            { 'name': 'punsh', 'duration': 100 }, 
            { 'name': 'kick', 'duration': 150 }, 
            { 'name': 'dash', 'duration': 75 }
        ]

        actions_2 = [
            { 'name': 'idle', 'duration': 100 }, 
            { 'name': 'run', 'duration': 100 }, 
            { 'name': 'jump', 'duration': 75 }, 
            { 'name': 'punsh', 'duration': 100 }, 
            { 'name': 'kick', 'duration': 100 }, 
            { 'name': 'dash', 'duration': 75 }
        ]

        attacks = [
            Attack('kick', 'kick', 10, 1, 0),
            Attack('punsh', 'punsh', 10, 1, 0),
            Attack('dash', 'dash', 10, 1, 0),
        ]

        player_images = { 'fallback': 'fallback.png', 'avatar': 'avatar.png' }
        
        self.arenas = [
            Arena("cave.png", (0,Settings.window_height - 50), [Settings.window_width,100]),
            Arena("dark_sandstone.png", (0,Settings.window_height - 50), [Settings.window_width,100]),
            Arena("light_sandstone.png", (0,Settings.window_height - 50), [Settings.window_width,100])
        ]
        
        self.player_1 = Player(1, Settings.player_health, Settings.player_size_1, (Settings.window_width // 4 - Settings.player_size_1[0] // 2, Settings.window_height - 50 - Settings.player_size_1[1]), False, player_images, actions_1, attacks, 10, (144, 200, 232))
        self.player_2 = Player(2, Settings.player_health, Settings.player_size_2, (Settings.window_width // 4 + Settings.window_width // 2 - Settings.player_size_2[0] // 2, Settings.window_height - 50 - Settings.player_size_2[1]), True, player_images, actions_2, attacks, 10, (112, 136, 136))
        
        self.players = pygame.sprite.Group(self.player_1, self.player_2)

        self.keyhandlers = []
        self.controllerhandlers = []

        # Player 1 Keybinds

        keybinds_1 = [
            KeyBind(pygame.KEYDOWN, pygame.K_d, 'movement', 'self.player_1.handle_movement', { 'direction': 'right', 'flip': False, 'animation': 'run' , 'loop': True }),
            KeyBind(pygame.KEYDOWN, pygame.K_a, 'movement', 'self.player_1.handle_movement', { 'direction': 'left', 'flip': True, 'animation': 'run' , 'loop': True }),
            KeyBind(pygame.KEYUP, pygame.K_d, 'movement', 'self.player_1.stop_handle_movement', { 'direction': 'right' }),
            KeyBind(pygame.KEYUP, pygame.K_a, 'movement', 'self.player_1.stop_handle_movement', { 'direction': 'left' }),
            KeyBind(pygame.KEYDOWN, pygame.K_1, 'attack', 'self.player_1.handle_attack', { 'type': 'punsh', 'animation': 'punsh' , 'loop': False }),
            KeyBind(pygame.KEYDOWN, pygame.K_2, 'attack', 'self.player_1.handle_attack', { 'type': 'kick', 'animation': 'kick' , 'loop': False }),
            KeyBind(pygame.KEYDOWN, pygame.K_3, 'attack', 'self.player_1.handle_attack', { 'type': 'dash', 'animation': 'dash' , 'loop': False }),
        ]
        self.keyhandlers.append(KeyHandler(self.player_1, keybinds_1))

        # Player 2 Keybinds

        keybinds_2 = [
            KeyBind(pygame.KEYDOWN, pygame.K_RIGHT, 'movement', 'self.player_2.handle_movement', { 'direction': 'right', 'flip': False, 'animation': 'run' , 'loop': True }),
            KeyBind(pygame.KEYDOWN, pygame.K_LEFT, 'movement', 'self.player_2.handle_movement', { 'direction': 'left', 'flip': True, 'animation': 'run' , 'loop': True }),
            KeyBind(pygame.KEYUP, pygame.K_RIGHT, 'movement', 'self.player_2.stop_handle_movement', { 'direction': 'right' }),
            KeyBind(pygame.KEYUP, pygame.K_LEFT, 'movement', 'self.player_2.stop_handle_movement', { 'direction': 'left' }),
            KeyBind(pygame.KEYDOWN, pygame.K_8, 'attack', 'self.player_2.handle_attack', { 'type': 'punsh', 'animation': 'punsh' , 'loop': False }),
            KeyBind(pygame.KEYDOWN, pygame.K_9, 'attack', 'self.player_2.handle_attack', { 'type': 'kick', 'animation': 'kick' , 'loop': False }),
            KeyBind(pygame.KEYDOWN, pygame.K_0, 'attack', 'self.player_2.handle_attack', { 'type': 'dash', 'animation': 'dash' , 'loop': False }),
        ]
        self.keyhandlers.append(KeyHandler(self.player_2, keybinds_2))

        keybinds_essential = [
            KeyBind(pygame.KEYDOWN, pygame.K_RETURN, 'essential', 'self.restart', None),
        ]
        self.keyhandlers.append(KeyHandler(None, keybinds_essential))

        if Settings.use_raspberry_pi:
            # Player 1 Controller Keybinds

            controllerbinds_1 = [
                ControllerBind(2, 'movement', 'self.player_1.handle_movement', { 'direction': 'left', 'flip': True, 'animation': 'run' , 'loop': True, 'stop_function': {'function': 'self.player_1.stop_handle_movement', 'payload': { 'direction': 'left' }} }),
                ControllerBind(3, 'movement', 'self.player_1.handle_movement', { 'direction': 'right', 'flip': False, 'animation': 'run' , 'loop': True, 'stop_function': {'function': 'self.player_1.stop_handle_movement', 'payload': { 'direction': 'right' } }}),
                
                ControllerBind(15, 'essential', 'self.restart', None),
                
                ControllerBind(4, 'attack', 'self.player_1.handle_attack', { 'type': 'punsh', 'animation': 'punsh' , 'loop': False, 'stop_function': None }),
                ControllerBind(14, 'attack', 'self.player_1.handle_attack', { 'type': 'kick', 'animation': 'kick' , 'loop': False, 'stop_function': None }),
            ]
            self.controllerhandlers.append(ControllerHandler(self.player_1, controllerbinds_1))

            # Player 2 Controller Keybinds

            controllerbinds_2 = [
                ControllerBind(0, 'movement', 'self.player_2.handle_movement', { 'direction': 'left', 'flip': True, 'animation': 'run' , 'loop': True, 'stop_function': {'function': 'self.player_2.stop_handle_movement', 'payload': { 'direction': 'left' }} }),
                ControllerBind(1, 'movement', 'self.player_2.handle_movement', { 'direction': 'right', 'flip': False, 'animation': 'run' , 'loop': True, 'stop_function': {'function': 'self.player_2.stop_handle_movement', 'payload': { 'direction': 'right' } }}),
                
                ControllerBind(5, 'essential', 'self.restart', None),
                
                ControllerBind(6, 'attack', 'self.player_2.handle_attack', { 'type': 'punsh', 'animation': 'punsh' , 'loop': False, 'stop_function': None }),
                ControllerBind(12, 'attack', 'self.player_2.handle_attack', { 'type': 'kick', 'animation': 'kick' , 'loop': False, 'stop_function': None }),
            ]
            self.controllerhandlers.append(ControllerHandler(self.player_2, controllerbinds_2))
        
        self.movement_timer = Timer(500)
        self.running = True
        
        self.restart()

    def run(self):
        while self.running:
            self.fps.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

    def update(self):
        self.players.update(self)
        self.overlay.update_healthbars(self.player_1, self.player_2)

    def draw(self):
        self.arena.draw(self.screen)
        self.players.draw(self.screen)
        self.overlay.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            for keyhandler in self.keyhandlers:
                for keybind in keyhandler.keybinds:
                    if keybind.type == 'essential' or not self.gameover:
                        if event.type == keybind.event:
                            if event.key == keybind.key:
                                if keybind.payload == None:
                                    eval(keybind.action + '()')
                                else:
                                    eval(f"{keybind.action}({keybind.payload})")

        for controllerhandler in self.controllerhandlers:
            for keybind in controllerhandler.keybinds:
                if keybind.type == 'essential' or not self.gameover:
                    if keybind.button.is_pressed:
                        if not keybind.pressed:
                            keybind.pressed = True
                            if keybind.payload == None:
                                eval(keybind.action + '()')
                            else:
                                eval(f"{keybind.action}({keybind.payload})")
                    else:
                        if keybind.pressed:
                            try:
                                if keybind.payload['stop_function']['function'] != None:
                                    if keybind.payload['stop_function']['payload'] != None:
                                        eval(f"{keybind.payload['stop_function']['function']}({keybind.payload['stop_function']['payload']})")
                                    else:
                                        eval(f"{keybind.payload['stop_function']['function']}()")
                            except:
                                pass
                            
                            keybind.pressed = False
                    
    def get_random_arena(self):
        arena = self.arenas[random.randint(0, len(self.arenas)-1)]
        return arena
    
    def restart(self):
        self.arena = self.get_random_arena()
        [ player.reset() for player in self.players.sprites() ]

        self.player_1.set_pos(Settings.window_width // 4 - Settings.player_size_1[0] // 2, Settings.window_height - 50 - Settings.player_size_1[1])
        self.player_2.set_pos(Settings.window_width // 4 + Settings.window_width // 2 - Settings.player_size_2[0] // 2, Settings.window_height - 50 - Settings.player_size_2[1])
        self.overlay = Overlay(self, self.player_1, self.player_2)
        self.overlay.header_text.update('Fight', (255,255,255), 50, Settings.window_width // 2)
        self.gameover = False


if __name__ == '__main__':
    game = Game()
    game.run()
