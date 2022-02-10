import pygame, os
from settings import Settings
from classes.background import Background
from classes.player import Player

class Game():
    def __init__(self):
        super().__init__()

        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        pygame.init()
        pygame.display.set_caption(Settings.title)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.fps = pygame.time.Clock()

        self.background = Background(Settings.background_image)
        self.player = Player(1, (250,250), 'fallback.png', ['idle', 'run'], 2, (144, 200, 232))
        self.running = True

    def run(self):
        while self.running:
            self.fps.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

    def update(self):
        self.player.update()

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.change_direction('right')
                    self.player.flip = True
                    self.player.action_manager.force_change_action('run', True)
                    self.player.start_moving()

                if event.key == pygame.K_a:
                    self.player.change_direction('left')
                    self.player.flip = False
                    self.player.action_manager.force_change_action('run', True)
                    self.player.start_moving()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    self.player.stop_moving()
                    self.player.action_manager.reset_action()
                    self.player.animation_set.change_current_animation(self.player.action_manager.current_action['name'])


if __name__ == '__main__':
    game = Game()
    game.run()
