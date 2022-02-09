import os,sys,glob

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings
from helpers.timer import Timer

class Animation():
    def __init__(self, animation_name, animation_path, animation_delay=200, default = False):
        super().__init__()
        self.animation_name = animation_name
        self.animation_path = animation_path
        self.default = default
        self.animation_delay = Timer(animation_delay)
        self.animation_frames = self.process_frames(self.get_frames(self.animation_path))

    def get_frames(self, animation_path):
        return glob.glob(os.path.join(Settings.path_image, str(animation_path) + "/*.png"))

    def process_frames(self, raw_frames):
        frames = [ os.path.basename(frame).split('.')[0] for frame in raw_frames ]
        frames.sort(key=int)
        return [ frame + '.png' for frame in frames ]