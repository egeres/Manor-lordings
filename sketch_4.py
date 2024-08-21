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

    def __init__(self, screen, terrain: Terrain, scale: int = 10):
        self.screen = screen
        self.terrain = terrain
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
                            entity.move_one_cell((1, 0))

    def events_mouse_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Adjust the mouse position based on the camera offset
        adjusted_x = mouse_x - self.camera_x
        adjusted_y = mouse_y - self.camera_y

        # Calculate the tile coordinates by dividing by the tile size
        tile_x = adjusted_x // self.tile_size
        tile_y = adjusted_y // self.tile_size

        # Ensure the coordinates are within the map boundaries
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

        clock = pygame.time.Clock()
        while self.running:
            self.events()
            self.draw()
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1500, 1500))

    t = Terrain((4, 4))
    Serf((0, 0), t)
    Serf((3, 3), t)
    renderer = Engine(screen, t, scale=15)
    renderer.start()
