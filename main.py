import pygame, os
from settings import Settings
from classes.player import Player
from classes.keyhandler import KeyHandler, KeyBind
from classes.arena import Arena

class Game():
    def __init__(self):
        super().__init__()

        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        pygame.init()
        pygame.display.set_caption(Settings.title)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.fps = pygame.time.Clock()

        self.arena = Arena(Settings.background_image, (0,Settings.window_height - 50), [Settings.window_width,100])
        self.player = Player(1, Settings.player_size, (Settings.window_width // 2 - Settings.player_size[0] // 2, Settings.window_height - 50 - Settings.player_size[1]), 'fallback.png', [{ 'name': 'idle', 'duration': 100 }, { 'name': 'run', 'duration': 100 }, { 'name': 'jump', 'duration': 75 }, { 'name': 'punsh', 'duration': 150 }, { 'name': 'kick', 'duration': 150 }], 10, (144, 200, 232))
        
        keybinds = [
            KeyBind(pygame.KEYDOWN, pygame.K_d, 'movement', 'self.player.handle_movement', { 'direction': 'right', 'flip': False, 'animation': 'run' , 'loop': True }),
            KeyBind(pygame.KEYDOWN, pygame.K_a, 'movement', 'self.player.handle_movement', { 'direction': 'left', 'flip': True, 'animation': 'run' , 'loop': True }),
            KeyBind(pygame.KEYDOWN, pygame.K_SPACE, 'movement', 'self.player.jump'),
            KeyBind(pygame.KEYUP, pygame.K_d, 'movement', 'self.player.stop_handle_movement', { 'direction': 'right' }),
            KeyBind(pygame.KEYUP, pygame.K_a, 'movement', 'self.player.stop_handle_movement', { 'direction': 'left' }),
            KeyBind(pygame.KEYDOWN, pygame.K_1, 'movement', 'self.player.handle_attack', { 'type': 'punsh', 'animation': 'punsh' , 'loop': False }),
            KeyBind(pygame.KEYDOWN, pygame.K_2, 'movement', 'self.player.handle_attack', { 'type': 'kick', 'animation': 'kick' , 'loop': False }),
        ]
        self.keyhandler = KeyHandler(self.player, keybinds)
        self.running = True

    def run(self):
        while self.running:
            self.fps.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

    def update(self):
        self.player.update(self)

    def draw(self):
        self.arena.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            for keybind in self.keyhandler.keybinds:
                if event.type == keybind.event:
                    if event.key == keybind.key:
                        if keybind.payload == None:
                            eval(keybind.action + '()')
                        else:
                            eval(f"{keybind.action}({keybind.payload})")

if __name__ == '__main__':
    game = Game()
    game.run()
