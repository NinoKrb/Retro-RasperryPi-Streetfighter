import os,sys,glob

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings

class Animation():
    def __init__(self, animation_name):
        super().__init__()
        self.animation_name = animation_name
        self.animation_frames = self.process_frames(self.get_frames(self.animation_name))

    def get_frames(self):
        return glob.glob(os.path.join(Settings.path_animation, str(self.animation_name) + "/*.png"))

    def process_frames(self, raw_frames):
        frames = [ os.path.basename(frame).split('.')[0] for frame in raw_frames ]
        frames.sort(key=int)
        return [ frame + '.png' for frame in frames ]