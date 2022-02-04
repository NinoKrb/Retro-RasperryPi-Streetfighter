import pygame, os
from settings import Settings
from classes.background import Background

class Game():
    def __init__(self):
        super().__init__()

        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        pygame.init()
        pygame.display.set_caption(Settings.title)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.fps = pygame.time.Clock()

        self.background = Background(Settings.background_image)
        self.running = True

    def run(self):
        while self.running:
            self.update()
            self.draw()

    def update(self):
        pass

    def draw(self):
        self.background.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
