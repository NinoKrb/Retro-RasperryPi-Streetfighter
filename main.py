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
        self.player = Player(1, (250,250), 'fallback.png', ['idle', 'run'])
        self.running = True

    def run(self):
        while self.running:
            self.update()
            self.draw()

    def update(self):
        self.player.update()

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
