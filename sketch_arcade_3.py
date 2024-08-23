# https://github.com/pythonarcade/arcade/issues/2353

from __future__ import annotations

import random
from pathlib import Path

import arcade
import arcade.color
import arcade.gui
import arcade.gui.widgets.buttons
import arcade.gui.widgets.layout
import arcade.gui.widgets.text
import arcade.key
from pyglet.math import Vec2

SCREEN_W = 1300
SCREEN_H = 1300
MOVEMENT_SPEED = 1
SIZE = 1
SPRITE_SIZE = 16 * SIZE

dir_art = Path(__file__).parent / "art"


class Terrain:

    def __init__(self, wh: tuple[int, int]) -> None:
        assert len(wh) == 2, "Width and height must be a tuple of 2 integers"
        self.width, self.height = wh
        self.tiles = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.entities: list[Entity] = []

        self.map = []
        for i in range(self.height):
            self.map.append([])
            for j in range(self.width):
                n = random.choice(["grass_dark_0", "grass_dark_1", "grass_dark_2"])
                if (i + j) % 2 == 0:
                    n = random.choice(
                        ["grass_light_0", "grass_light_1", "grass_light_2"]
                    )
                self.map[i].append(n)

        self.prepare_sprite()

    def add(self, entity: Entity) -> None:
        self.entities.append(entity)
        entity.terrain = self

    def prepare_sprite(self):
        self.sprite = arcade.SpriteList()
        for row_index, row in enumerate(self.map):
            for col_index, tile in enumerate(row):
                sprite = arcade.Sprite(str(dir_art / f"{tile}.png"), SIZE)
                sprite.center_x = col_index * SPRITE_SIZE + SPRITE_SIZE // 2
                sprite.center_y = row_index * SPRITE_SIZE + SPRITE_SIZE // 2
                self.sprite.append(sprite)

        # Bottom stuff
        for col_index in range(self.width):
            sprite = arcade.Sprite(str(dir_art / "undergroud_tile.png"), SIZE)
            sprite.center_x = col_index * SPRITE_SIZE + SPRITE_SIZE // 2
            sprite.center_y = -SPRITE_SIZE // 2
            self.sprite.append(sprite)

    def get_entity_at(self, x: int, y: int) -> Entity | None:
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        return None


class Entity:
    def __init__(self, pos: tuple[int, int]):
        self._x, self._y = pos
        self.terrain: Terrain | None = None

        self._sprite: arcade.Sprite | None = None
        self.sprite_index: int | None = None
        self.sprite_group: arcade.SpriteList | None = None

    def sprite_update(self):
        sprite = self.sprite
        if (
            self.sprite_group is not None
            and self.sprite_index is not None
            and sprite is not None
        ):
            self.sprite_group[self.sprite_index] = self.sprite

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        self._sprite = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if self.sprite is not None:
            self.sprite.center_x = value * SPRITE_SIZE + SPRITE_SIZE // 2

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if self.sprite is not None:
            self.sprite.center_y = value * SPRITE_SIZE + SPRITE_SIZE // 2

    def tick(self):
        raise NotImplementedError


class NaturalResource(Entity):
    pass


class Forest(NaturalResource):

    def __init__(self, x: int, y: int):
        super().__init__((x, y))

        # Internal data
        self._resources: int = 2

        # Sprite bs
        self.sprites = {
            "0": arcade.Sprite(str(dir_art / "entity_forest_0.png"), SIZE),
            "1": arcade.Sprite(str(dir_art / "entity_forest_1.png"), SIZE),
            "2": arcade.Sprite(str(dir_art / "entity_forest_2.png"), SIZE),
            "3": arcade.Sprite(str(dir_art / "entity_forest_3.png"), SIZE),
        }
        for s in self.sprites.values():
            s.center_x = x * SPRITE_SIZE + SPRITE_SIZE // 2
            s.center_y = y * SPRITE_SIZE + SPRITE_SIZE // 2

    @property
    def sprite(self):
        if self.resources == 0:
            return self.sprites["3"]
        elif self.resources == 1:
            return self.sprites["2"]
        elif self.resources == 2:
            return self.sprites["1"]
        else:
            return self.sprites["0"]

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, value):
        self._resources = value
        self.sprite_update()

    def tick(self):
        self.resources -= 1
        if self.resources < 0:
            self.resources = 0


class OrganicLifeForm(Entity):
    pass
    # Can move, but only within the map


class Serf(OrganicLifeForm):
    max_health = 3

    def __init__(self, x: int, y: int):
        super().__init__((x, y))
        self.sprite = arcade.Sprite(str(dir_art / "overlay_serf_0.png"), SIZE)
        self.sprite.center_x = x * SPRITE_SIZE + SPRITE_SIZE // 2
        self.sprite.center_y = y * SPRITE_SIZE + SPRITE_SIZE // 2

    def tick(self):
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_W, SCREEN_H, "Sprite Example")  # type: ignore

        # Terrain
        self.terrain = Terrain((4, 4))
        self.terrain.add(Serf(0, 0))
        self.terrain.add(Forest(1, 1))
        self.terrain.add(Forest(1, 2))
        self.terrain.add(Forest(2, 1))
        self.terrain.add(Forest(2, 2))

        # Gameplay
        self.turn: int = 0
        self.selected_tile: tuple[int, int] | None = None

        # Camera
        self.camera = arcade.Camera2D()
        self.camera.zoom = 10
        self.camera.bottom_left = Vec2(
            (-(SCREEN_W / 10) // 2) + (self.terrain.width * SPRITE_SIZE // 2),
            (-(SCREEN_H / 10) // 2) + (self.terrain.height * SPRITE_SIZE // 2),
        )
        self.keys = {"w": False, "a": False, "s": False, "d": False}

        # UI
        arcade.load_font(dir_art / "EXEPixelPerfect.ttf")
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        self.top_label = arcade.gui.UILabel(
            text="0123456789QWERTYUIOPASDFGHJKLMNBVCXZ",
            width=300,
            font_size=60,
            align="center",
            font_name="EXEPixelPerfect",
        )
        self.button_next = arcade.gui.UIFlatButton(text="Next", width=200, height=50)
        self.button_next.on_click = self.gameplay_next_turn
        l = arcade.gui.widgets.layout.UIAnchorLayout()
        l.add(self.top_label, anchor_y="top")
        l.add(self.button_next, anchor_y="bottom")
        self.ui.add(l)

        # Sprites
        self.sprite_selected = arcade.Sprite(str(dir_art / "selected.png"))
        self.sprites_selected = arcade.SpriteList()
        self.sprites_selected.append(self.sprite_selected)
        self.sprites_entities = arcade.SpriteList()
        for n, entity in enumerate(self.terrain.entities):
            if entity.sprite is not None:
                self.sprites_entities.append(entity.sprite)
                entity.sprite_index = n
                entity.sprite_group = self.sprites_entities

    def gameplay_next_turn(self, event):
        for entity in self.terrain.entities:
            entity.tick()
        self.turn += 1

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.terrain.sprite.draw(pixelated=True)
        self.sprites_entities.draw(pixelated=True)
        if self.selected_tile:
            x, y = self.selected_tile
            self.sprite_selected.center_x = x * SPRITE_SIZE + SPRITE_SIZE // 2
            self.sprite_selected.center_y = y * SPRITE_SIZE + SPRITE_SIZE // 2
            self.sprites_selected.draw(pixelated=True)
        self.ui.draw()

    def on_update(self, delta_time):
        x, y = 0, 0
        if self.keys["w"]:
            y = 1
        if self.keys["s"]:
            y = -1
        if self.keys["a"]:
            x = -1
        if self.keys["d"]:
            x = 1
        v = Vec2(x, y).normalize() * MOVEMENT_SPEED
        self.camera.position = self.camera.position + v

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

    def on_mouse_press(self, x, y, button, modifiers):
        tx = int(((x // 10) + self.camera.bottom_left.x) // SPRITE_SIZE)
        ty = int(((y // 10) + self.camera.bottom_left.y) // SPRITE_SIZE)
        if 0 <= tx < len(self.terrain.tiles[0]) and 0 <= ty < len(self.terrain.tiles):
            self.selected_tile = (tx, ty)
            if e := self.terrain.get_entity_at(tx, ty):
                self.top_label.text = f"{e.__class__.__name__}"
            else:
                self.top_label.text = f"Grass tile"
        else:
            self.selected_tile = None
            self.top_label.text = f"-"


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
