import pygame, os
from settings import Settings
from classes.background import Background
from classes.player import Player
from classes.floor import Floor
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
        self.player = Player(1, Settings.player_size, (Settings.window_width // 2 - Settings.player_size[0] // 2, Settings.window_height - 50 - Settings.player_size[1]), 'fallback.png', [{ 'name': 'idle', 'duration': 100 }, { 'name': 'run', 'duration': 100 }, { 'name': 'jump', 'duration': 75 }], 10, (144, 200, 232))
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    if event.key == pygame.K_a:
                        self.player.change_direction('left')
                        self.player.flip = True
                    else:
                        self.player.change_direction('right')
                        self.player.flip = False
                    self.player.move_direction()
                    self.player.action_manager.force_change_action('run', True)
                    self.player.animation_set.change_current_animation(self.player.action_manager.current_action['name'])

                if event.key == pygame.K_SPACE:
                    self.player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    if event.key == pygame.K_d:
                        self.player.stop_move_direction('right')
                    else:
                        self.player.stop_move_direction('left')

                    if not self.player.is_jumping:
                        self.player.action_manager.reset_action()
                        self.player.action_manager.clear_queue()
                    self.player.animation_set.change_current_animation(self.player.action_manager.current_action['name'])


if __name__ == '__main__':
    game = Game()
    game.run()
