import arcade
from pathlib import Path

# Define the path to the image
image_path = Path(r"C:\Github\Manor-lordings\art\grass_dark_0.png")

# Constants for the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Display an Image"
SCALE = 10  # Scale factor to enlarge the 16x16 image


# Define a class for the game window
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Load the image and set the scale
        self.texture = arcade.load_texture(image_path, can_cache=False)
        # self.scale = 10

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draw the image in the center of the screen
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            self.texture.width * SCALE,
            self.texture.height * SCALE,
            self.texture,
        )


# Start the game
if __name__ == "__main__":
    window = MyGame()
    arcade.run()
