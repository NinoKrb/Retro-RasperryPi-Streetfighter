import os

class Settings():
    window_height = 825
    window_width = 1375

    # Base paths
    base_file = os.path.dirname(os.path.abspath(__file__))
    asset_file = os.path.join(base_file, "assets")

    # Folder paths
    path_image = os.path.join(asset_file, "images")
    path_storage = os.path.join(base_file, "storage")

    title = "Streetfighter - RaspberryPi"
    fps = 60

    # Assets
    background_image = "background.png"
