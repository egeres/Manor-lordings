from __future__ import annotations

import random
from abc import ABC, abstractmethod
from pathlib import Path

import pygame

dir_root_art = Path("/mnt/c/Github/Manor-lordings/art")


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_path: str, pos: tuple[int, int], scale: int = 1):
        assert isinstance(scale, int), "Scale must be an integer"
        assert scale > 0, "Scale must be greater than 0"
        super().__init__()

        image_path = str(dir_root_art / (image_path + ".png"))
        self.original_image = pygame.image.load(image_path).convert_alpha()
        width, height = self.original_image.get_size()
        scaled_width, scaled_height = width * scale, height * scale
        self.image = pygame.transform.scale(
            self.original_image, (scaled_width, scaled_height)
        )
        self.rect = self.image.get_rect(topleft=pos)


class Entity(ABC):

    def __init__(
        self,
        pos: tuple[int, int],
        terrain: Terrain | None = None,
    ) -> None:
        assert len(pos) == 2, "Position must be a tuple of 2 integers"
        assert isinstance(terrain, Terrain), "Terrain must be an instance of Terrain"

        self.terrain = terrain
        if self.terrain is not None and not (
            0 <= pos[0] < self.terrain.width and 0 <= pos[1] < self.terrain.height
        ):
            raise ValueError("Position is outside the terrain boundaries")
        self.x, self.y = pos
        self.terrain.entities.append(self)

        self.sprite: MySprite | None = None

    @abstractmethod
    def render(self) -> str: ...


class OrganicLifeForm(Entity):
    pass

    def move_one_cell(self, direction: tuple[int, int]) -> bool:
        """Returns if the action was completed"""

        assert len(direction) == 2, "Direction must be a tuple of 2 integers"
        assert direction in [(0, 1), (0, -1), (1, 0), (-1, 0)], "Invalid direction"

        new_x, new_y = self.x + direction[0], self.y + direction[1]
        # if 0 <= new_x < self.terrain.width and 0 <= new_y < self.terrain.height:
        #     self.x, self.y = new_x, new_y
        #     return True
        # else:
        #     print("Cannot move outside the terrain boundaries")
        #     return False

        self.x, self.y = new_x, new_y
        return True


class Serf(OrganicLifeForm):
    max_health = 3

    def render(self) -> str:
        return "organiclifeform_serf_0"


class Terrain:

    def __init__(self, wh: tuple[int, int]) -> None:
        assert len(wh) == 2, "Width and height must be a tuple of 2 integers"
        self.width, self.height = wh
        self.tiles = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.entities: list[Entity] = []

        self.sprites_tiles = []
        for i in range(self.height):
            self.sprites_tiles.append([])
            for j in range(self.width):
                n = random.choice(["grass_dark_0", "grass_dark_1", "grass_dark_2"])
                if (i + j) % 2 == 0:
                    n = random.choice(
                        ["grass_light_0", "grass_light_1", "grass_light_2"]
                    )
                self.sprites_tiles[i].append(n)

    def add_entity(self, entity: Entity) -> None:
        entity.terrain = self
        self.entities.append(entity)


class Engine:

    def __init__(
        self,
        screen,
        terrain: Terrain,
        uielements: list[UIElement],
        scale: int = 10,
    ):
        self.screen = screen
        self.terrain = terrain
        self.uielements = uielements
        self.scale = scale

        self.camera_x, self.camera_y = 0, 0
        self.selectedtile: tuple[int, int] | None = None
        self.tile_size = 16 * self.scale
        self.running = True

    def events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.camera_x += 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.camera_x -= 10
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.camera_y += 10
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.camera_y -= 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.events_mouse_click()

            # Just a temporary test
            if event.type == pygame.KEYUP:
                if keys[pygame.K_t]:
                    print("Moving entities")
                    for entity in self.terrain.entities:
                        if isinstance(entity, Serf):
                            entity.move_one_cell((1, 0))x

    def events_mouse_click(self):

        mouse_pos = pygame.mouse.get_pos()

        # 🍑 UI click
        for element in self.uielements:
            element.process_click(mouse_pos)
            # if element.visibility == "visible" and element.clicable:
            #     if element.rect.collidepoint(pygame.mouse.get_pos()):
            #         element.on_click()
            #         break

        # 🍑 Terrain click
        mouse_x, mouse_y = mouse_pos
        adjusted_x = mouse_x - self.camera_x
        adjusted_y = mouse_y - self.camera_y
        tile_x = adjusted_x // self.tile_size
        tile_y = adjusted_y // self.tile_size
        if 0 <= tile_x < self.terrain.width and 0 <= tile_y < self.terrain.height:
            print(f"Clicked tile coordinates: ({tile_x}, {tile_y})")
            self.selectedtile = (tile_x, tile_y)
        else:
            print("Clicked outside the map.")
            self.selectedtile = None

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Background
        for sprite in self.spritegroup_terrain_background:
            adjusted_rect = sprite.rect.move(self.camera_x, self.camera_y)
            self.screen.blit(sprite.image, adjusted_rect)

        # Entities
        for entity in self.terrain.entities:
            if entity.sprite is None:
                continue
            entity.sprite.rect.topleft = (
                entity.x * self.tile_size + self.camera_x,
                entity.y * self.tile_size + self.camera_y,
            )
            self.screen.blit(entity.sprite.image, entity.sprite.rect)

        # Selected tile
        if self.selectedtile:
            self.sprite_selected.rect.topleft = (
                self.selectedtile[0] * self.tile_size + self.camera_x,
                self.selectedtile[1] * self.tile_size + self.camera_y,
            )
            self.screen.blit(self.sprite_selected.image, self.sprite_selected.rect)

        # UI elements
        for element in self.uielements:
            element.render(screen)

        pygame.display.flip()

    def start(self):

        # Sprites: Background
        self.spritegroup_terrain_background = pygame.sprite.Group()
        for y, row in enumerate(self.terrain.sprites_tiles):
            for x, tile in enumerate(row):
                pos = (x * 16 * self.scale, y * 16 * self.scale)
                sprite = MySprite(tile, pos, self.scale)
                self.spritegroup_terrain_background.add(sprite)

        # Sprites: Entities
        for entity in self.terrain.entities:
            pos = (entity.x * 16 * self.scale, entity.y * 16 * self.scale)
            sprite = MySprite(entity.render(), pos, self.scale)
            entity.sprite = sprite

        # Sprites: Selected
        self.sprite_selected = MySprite("selected", (0, 0), self.scale)

        # # Sprite: UI elements
        # for element in self.uielements:
        #     element.sprite = MySprite(element.image, (0, 0), self.scale)

        clock = pygame.time.Clock()
        while self.running:
            self.events()
            self.draw()
            clock.tick(60)
        pygame.quit()


# Buttom_1 = Button(
#     "image",
#     on_click = method(),
#     "sound",
#     ...
# )
# a = Container(color_red, 2px,
#     [
#         Buttom_1,
#         Buttom_2,
#     ]
# )
# a.position = (0, 100)
# a.position = "bottom_center ?"


class UIElement:

    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position
        self.clicable: bool = False

        self.visibility = "visible"
        self.sprite: MySprite | None = None
        self.width: int | None = None
        self.height: int | None = None
        self.image: str | None = None
        self.parent: UIElement | None = None

    def set_visibility(self, visibility: str) -> None:
        assert visibility in [
            "visible",
            "hidden",
            "disabled",
        ], "Invalid visibility value"
        self.visibility = visibility

    def on_click(self) -> None:
        pass

    @property
    def x(self) -> int:
        to_return = self.position[0]
        if self.parent is not None:
            to_return += self.parent.x
        return to_return

    @property
    def y(self) -> int:
        to_return = self.position[1]
        if self.parent is not None:
            to_return += self.parent.y
        return to_return

    def render(self, screen) -> None:
        raise NotImplementedError

    @property
    def rect(self) -> pygame.Rect:
        raise NotImplementedError
    

    def process_click(self, mouse_pos: tuple[int, int]) -> None:
        raise NotImplementedError


class Container(UIElement):

    def __init__(
        self,
        position: tuple[int, int],
        color: str,
        border_width: int,
        elements: list[UIElement],
    ) -> None:
        super().__init__(position)

        self.color = color
        self.border_width = border_width
        self.elements = elements
        for element in elements:
            element.parent = self

    def render(self, screen) -> None:
        for element in self.elements:
            element.render(screen)

    @property
    def rect(self) -> pygame.Rect:
        raise NotImplementedError


class TextLabel(UIElement):

    def __init__(
        self,
        position: tuple[int, int],
        text: str,
        font: str = "EXEPixelPerfect.ttf",
        size: int = 60,
    ) -> None:
        super().__init__(position)

        self._text = text
        self.font_pygame = pygame.font.Font(str(dir_root_art / font), size)
        self.text_surface = self.font_pygame.render(
            text, True, (255, 255, 255), (10, 10, 10)
        )
        self._rect = self.text_surface.get_rect()

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self.text_surface = self.font_pygame.render(
            self._text, True, (255, 255, 255), (10, 10, 10)
        )

    def render(self, screen) -> None:
        screen.blit(self.text_surface, (self.x, self.y))


class Button(UIElement):

    def __init__(
        self,
        position: tuple[int, int],
        image: str,
        on_click,
        sound: str | None = None,
        scale: int = 1,
    ) -> None:
        super().__init__(position)

        self.image = image
        self.on_click = on_click
        self.sound = sound
        self.clicable = True

        self.sprite: MySprite = MySprite(image, (0, 0), scale)
        self.width, self.height = self.sprite.rect.size

    def render(self, screen) -> None:
        screen.blit(self.sprite.image, (self.x, self.y))

    @property
    def rect(self) -> pygame.Rect:
        return self.sprite.rect


# TODO_2: Add python colour or something
# TODO_2: Add

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1500, 1500))

    # container = Container("red", 2, [a])

    label_0 = TextLabel((0, 0), "Hello, World!")
    button_0 = Button(
        (0, 100),
        "ui_button_nextturn",
        on_click=lambda: print("Hello, World!"),
        scale=15,
    )
    container = Container((10, 10), "red", 2, [label_0, button_0])

    t = Terrain((4, 4))
    Serf((0, 0), t)
    Serf((3, 3), t)
    renderer = Engine(screen, t, [container], scale=15)
    renderer.start()
