import os,sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from classes.floor import Floor
from classes.background import Background

class Arena():
    def __init__(self, image, floor_pos, floor_size):
        self.image = image
        self.floor_pos = floor_pos
        self.floor_size = floor_size
        self.floor = Floor((floor_pos), floor_size)
        self.background = Background(image)

    def draw(self, screen):
        self.background.draw(screen)
        self.floor.draw(screen)
