""" Sprite Sample Program """

from __future__ import annotations

from pathlib import Path
import arcade
import arcade.color
import arcade.gui
import arcade.key

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1300
MOVEMENT_SPEED = 5
SIZE = 10
SPRITE_SIZE = 16 * SIZE


class MapEntity:

    def __init__(self, image_path: str, pos):
        self.image_path = image_path
        self._x, self._y = pos
        self.sprite: arcade.Sprite | None = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.sprite.center_x = value * SPRITE_SIZE + SPRITE_SIZE // 2

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.sprite.center_y = value * SPRITE_SIZE + SPRITE_SIZE // 2


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")
        self.group_background = None
        self.player_sprite = None
        self.camera = None
        self.camera_x = 0
        self.camera_y = 0
        self.keys = {"w": False, "a": False, "s": False, "d": False}
        arcade.set_background_color(arcade.color.BLACK)
        self.counter = 0
        self.selected_tile: tuple[int, int] | None = None

        def increase_counter(event):
            self.counter += 1
            self.my_label.text = f"Counter: {self.counter}"

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        # my_button = arcade.gui.UIFlatButton(text="Click Me", width=200)
        # my_button.on_click = increase_counter
        # self.my_label = arcade.gui.UILabel(text="Hello World", width=300, font_size=40)
        # self.v_box = arcade.gui.UIBoxLayout()
        # self.v_box.add(my_button)
        # self.v_box.add(self.my_label)
        # self.ui_manager.add(
        #     arcade.gui.UIAnchorWidget(
        #         anchor_x="center_x", anchor_y="center_y", child=self.v_box
        #     )
        # )
        self.top_label = arcade.gui.UILabel(
            text="-", width=300, font_size=40, align="center"
        )
        bordered_label = arcade.gui.UIBorder(
            self.top_label, border_width=10, bg_color=(*arcade.color.BLACK, 255)
        )
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="top", align_y=-50, child=bordered_label
            )
        )

    def setup(self):

        dir_art = Path("C:/Github/Manor-lordings/art")

        # Load the tile map
        self.map = [
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
        ]

        self.entities = [
            MapEntity("overlay_serf_0", (0, 0)),
            MapEntity("overlay_serf_0", (2, 2)),
        ]

        # Load the sprite textures
        texture_paths = {
            "grass_dark_0": dir_art / "grass_dark_0.png",
            "grass_light_0": dir_art / "grass_light_0.png",
            "overlay_serf_0": dir_art / "overlay_serf_0.png",
        }

        self.group_background = arcade.SpriteList()
        for row_index, row in enumerate(self.map):
            for col_index, tile in enumerate(row):
                texture = texture_paths[tile]
                sprite = arcade.Sprite(texture, SIZE)
                sprite.center_x = col_index * SPRITE_SIZE + SPRITE_SIZE // 2
                sprite.center_y = row_index * SPRITE_SIZE + SPRITE_SIZE // 2
                self.group_background.append(sprite)

        # self.group_serfs = arcade.SpriteList()
        # for entity in self.entities:
        #     serf_sprite = arcade.Sprite(texture_paths[entity.image_path], SIZE)
        #     serf_sprite.center_x = entity.x * SPRITE_SIZE + SPRITE_SIZE // 2
        #     serf_sprite.center_y = entity.y * SPRITE_SIZE + SPRITE_SIZE // 2
        #     self.group_serfs.append(serf_sprite)
        for entity in self.entities:
            serf_sprite = arcade.Sprite(texture_paths[entity.image_path], SIZE)
            serf_sprite.center_x = entity.x * SPRITE_SIZE + SPRITE_SIZE // 2
            serf_sprite.center_y = entity.y * SPRITE_SIZE + SPRITE_SIZE // 2
            entity.sprite = serf_sprite

        # Initialize the camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Sprite for "selected" tile
        self.sprite_selected = arcade.Sprite(dir_art / "selected.png", SIZE)

    def on_draw(self):
        arcade.start_render()

        self.camera.use()

        self.group_background.draw(pixelated=True)

        if self.selected_tile:
            x, y = self.selected_tile
            self.sprite_selected.center_x = x * SPRITE_SIZE + SPRITE_SIZE // 2
            self.sprite_selected.center_y = y * SPRITE_SIZE + SPRITE_SIZE // 2
            self.camera.use()
            self.sprite_selected.draw(pixelated=True)

        for entity in self.entities:
            entity.sprite.draw(pixelated=True)

        self.ui_manager.draw()

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
        # elif key == arcade.key.T:
        #     self.counter += 1  # Increase the counter when "t" is pressed
        # elif key == arcade.key.Y:
        #     self.camera.zoom(1.1)  # Zoom in when "y" is pressed
        elif key == arcade.key.T:
            self.entities[0].x += 1
            # self.entities[0].sprite.center_x += SPRITE_SIZE

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.keys["w"] = False
        elif key == arcade.key.S:
            self.keys["s"] = False
        elif key == arcade.key.A:
            self.keys["a"] = False
        elif key == arcade.key.D:
            self.keys["d"] = False

    def on_mouse_press(self, x, y, button, modifiers):
        # Get the world coordinates from the mouse position and camera offset
        world_x = x + self.camera_x
        world_y = y + self.camera_y

        # Convert the world coordinates to tile coordinates
        tile_x = int(world_x // SPRITE_SIZE)
        tile_y = int(world_y // SPRITE_SIZE)

        # Ensure the click is within the map boundaries
        if 0 <= tile_x < len(self.map[0]) and 0 <= tile_y < len(self.map):
            print(f"Tile clicked: ({tile_x}, {tile_y})")
            self.selected_tile = (tile_x, tile_y)
        else:
            print("Click outside the map")
            self.selected_tile = None


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
