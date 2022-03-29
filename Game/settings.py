import os

class Settings():
    window_height = 825
    window_width = 1375

    # Base paths
    base_file = os.path.dirname(os.path.abspath(__file__))
    asset_file = os.path.join(base_file, "assets")

    # Folder paths
    path_image = os.path.join(asset_file, "images")
    path_font = os.path.join(asset_file, "fonts")
    path_storage = os.path.join(asset_file, "storage")

    # Specific paths
    path_background = os.path.join(path_image, "backgrounds")
    path_player = os.path.join(path_image, "players")

    title = "Streetfighter - RaspberryPi"
    fps = 60

    # Assets
    background_image = "background.png"

    use_raspberry_pi = False

    # Player
    player_size_1 = (250,250)
    player_size_2 = (200,200)
    player_default_direction = "right"
    player_speed = 6
    player_sprinting_speed = 10
    player_default_lifes = 3
    player_animation_delay = 100
    player_jump_height = -10
    player_jump_instant_move = 10
    player_y_momentum = 0.5
    player_max_y_momentum = 10
    player_max_jumps = 2
    player_health = 1000
    player_collide_ratio = 0.55

    # Overlay
    avatar_size = (50,50)
    healthbar_height = 25
    healthbar_health_color = (201, 54, 54)
    healthbar_blank_color = (199, 199, 199)
    healthbar_width_factor = 3