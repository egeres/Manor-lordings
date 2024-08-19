import pygame
from pathlib import Path


dir_root_art = Path("/mnt/c/Github/Manor-lordings/art")


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_path: str, pos, scale: int = 1):
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


class Renderer:

    def __init__(self, scale: int = 10):
        self.scale = scale
        self.camera_x = 0
        self.camera_y = 0

        self.tile_size = 16 * self.scale

        self.map = [
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
        ]

        self.selected_tile: tuple[int, int] | None = None

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((1500, 1500))

        sprite_group_background = pygame.sprite.Group()
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                # file_path = f"/mnt/c/Github/Manor-lordings/art/{tile}.png"
                pos = (x * 16 * self.scale, y * 16 * self.scale)
                sprite = MySprite(tile, pos, self.scale)
                sprite_group_background.add(sprite)

        # Sprite selected tile
        sprite_selected = MySprite("select", (0, 0), self.scale)

        # Main game loop
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_mouse_click()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.camera_x += 10
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.camera_x -= 10
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.camera_y += 10
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.camera_y -= 10

            screen.fill((0, 0, 0))

            # Draw background with camera offset
            for sprite in sprite_group_background:
                adjusted_rect = sprite.rect.move(self.camera_x, self.camera_y)
                screen.blit(sprite.image, adjusted_rect)

            # Draw selected tile
            if self.selected_tile:
                x, y = self.selected_tile
                pos = (x * 16 * self.scale, y * 16 * self.scale)

                adjusted_pos = (pos[0] + self.camera_x, pos[1] + self.camera_y)

                sprite_selected.rect.topleft = adjusted_pos
                screen.blit(sprite_selected.image, sprite_selected.rect)

            pygame.display.flip()
            clock.tick(60)  # Cap the frame rate to 60 FPS
        pygame.quit()

    def handle_mouse_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Adjust the mouse position based on the camera offset
        adjusted_x = mouse_x - self.camera_x
        adjusted_y = mouse_y - self.camera_y

        # Calculate the tile coordinates by dividing by the tile size
        tile_x = adjusted_x // self.tile_size
        tile_y = adjusted_y // self.tile_size

        # Ensure the coordinates are within the map boundaries
        if 0 <= tile_x < len(self.map[0]) and 0 <= tile_y < len(self.map):
            print(f"Clicked tile coordinates: ({tile_x}, {tile_y})")
            self.selected_tile = (tile_x, tile_y)
        else:
            print("Clicked outside the map.")
            self.selected_tile = None


if __name__ == "__main__":
    renderer = Renderer()
    renderer.start()
