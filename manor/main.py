import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, scale: int = 1):
        assert isinstance(scale, int), "Scale must be an integer"
        assert scale > 0, "Scale must be greater than 0"
        super().__init__()
        # Load image
        self.original_image = pygame.image.load(image_path).convert_alpha()

        # Scale the image
        width, height = self.original_image.get_size()
        scaled_width, scaled_height = width * scale, height * scale
        self.image = pygame.transform.scale(
            self.original_image, (scaled_width, scaled_height)
        )

        # Get position and update rect accordingly
        self.rect = self.image.get_rect(topleft=pos)


class Renderer:

    def __init__(self, scale: int = 10):
        self.scale = scale

        self.map = [
            ["grass", "debug", "grass", "grass"],
            ["grass", "debug", "grass", "grass"],
            ["grass", "grass", "debug", "grass"],
            ["grass", "grass", "grass", "grass"],
        ]

    def start(self):
        pygame.init()

        screen = pygame.display.set_mode((1500, 1500))

        sprite_group = pygame.sprite.Group()

        # sprite1 = MySprite(
        #     "/mnt/c/Github/Manor-lordings/art/grass_tile_0.png", (0, 0), self.scale
        # )
        # sprite_group.add(sprite1)

        # Loop over the map to create sprites for each tile
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                file_path = "/mnt/c/Github/Manor-lordings/art/debug.png"
                if tile == "grass":
                    file_path = "/mnt/c/Github/Manor-lordings/art/grass_tile_0.png"
                # Calculate the position of the tile
                pos = (x * 16 * self.scale, y * 16 * self.scale)
                # Create a new sprite for the grass tile
                sprite = MySprite(file_path, pos, self.scale)
                sprite_group.add(sprite)

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear screen
            screen.fill((0, 0, 0))

            # Draw sprites
            sprite_group.draw(screen)

            # Update the display
            pygame.display.flip()

        # Quit pygame
        pygame.quit()


if __name__ == "__main__":

    renderer = Renderer()
    renderer.start()
