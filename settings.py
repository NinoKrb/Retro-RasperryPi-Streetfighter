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

    # Specific paths
    path_background = os.path.join(path_image, "backgrounds")
    path_player = os.path.join(path_image, "players")

    title = "Streetfighter - RaspberryPi"
    fps = 60

    # Assets
    background_image = "background.png"

    # Player
    player_size = (250,250)
    player_default_direction = "right"
    player_size = (40,55)
    player_speed = 6
    player_sprinting_speed = 10
    player_default_lifes = 3
    player_animation_delay = 100
    player_jump_height = -10
    player_jump_instant_move = 10
    player_y_momentum = 0.5
    player_max_y_momentum = 10
    player_max_jumps = 2