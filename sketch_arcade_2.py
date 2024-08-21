""" Sprite Sample Program """

import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5
SIZE = 10
SPRITE_SIZE = 16 * SIZE


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")
        self.player_list = None
        self.player_sprite = None
        self.camera = None
        self.camera_x = 0
        self.camera_y = 0
        self.keys = {"w": False, "a": False, "s": False, "d": False}
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        # self.player_list = arcade.SpriteList()
        # a = r"C:\Github\Manor-lordings\art\grass_dark_0.png"
        # self.player_sprite = arcade.Sprite(a, 10)
        # self.player_sprite.center_x = 50
        # self.player_sprite.center_y = 50
        # self.player_list.append(self.player_sprite)

        self.player_list = arcade.SpriteList()

        # Load the tile map
        self.map = [
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
        ]

        # Load the sprite textures
        texture_paths = {
            "grass_dark_0": r"C:\Github\Manor-lordings\art\grass_dark_0.png",
            "grass_light_0": r"C:\Github\Manor-lordings\art\grass_light_0.png",
        }

        # Loop over the map and create the sprites
        for row_index, row in enumerate(self.map):
            for col_index, tile in enumerate(row):
                texture = texture_paths[tile]
                sprite = arcade.Sprite(texture, SIZE)
                sprite.center_x = col_index * SPRITE_SIZE + SPRITE_SIZE // 2
                sprite.center_y = row_index * SPRITE_SIZE + SPRITE_SIZE // 2
                self.player_list.append(sprite)

        # Initialize the camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()

        # Set the camera position
        self.camera.use()

        # Draw all sprites
        self.player_list.draw(pixelated=True)

    def on_update(self, delta_time):
        if self.keys["w"]:
            self.camera_y += MOVEMENT_SPEED
        if self.keys["s"]:
            self.camera_y -= MOVEMENT_SPEED
        if self.keys["a"]:
            self.camera_x -= MOVEMENT_SPEED
        if self.keys["d"]:
            self.camera_x += MOVEMENT_SPEED

        self.camera.move_to((self.camera_x, self.camera_y), 1)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.keys["w"] = True
        elif key == arcade.key.S:
            self.keys["s"] = True
        elif key == arcade.key.A:
            self.keys["a"] = True
        elif key == arcade.key.D:
            self.keys["d"] = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.keys["w"] = False
        elif key == arcade.key.S:
            self.keys["s"] = False
        elif key == arcade.key.A:
            self.keys["a"] = False
        elif key == arcade.key.D:
            self.keys["d"] = False


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
