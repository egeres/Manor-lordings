import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, scale: int = 1):
        assert isinstance(scale, int), "Scale must be an integer"
        assert scale > 0, "Scale must be greater than 0"
        super().__init__()
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

        self.map = [
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
            ["grass_dark_0", "grass_light_0", "grass_dark_0", "grass_light_0"],
            ["grass_light_0", "grass_dark_0", "grass_light_0", "grass_dark_0"],
        ]

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((1500, 1500))

        sprite_group_background = pygame.sprite.Group()
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                file_path = f"/mnt/c/Github/Manor-lordings/art/{tile}.png"
                pos = (x * 16 * self.scale, y * 16 * self.scale)
                sprite = MySprite(file_path, pos, self.scale)
                sprite_group_background.add(sprite)

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            sprite_group_background.draw(screen)
            sprite = MySprite(
                "/mnt/c/Github/Manor-lordings/art/overlay_serf_0.png",
                (0, 0),
                self.scale,
            )
            screen.blit(sprite.image, sprite.rect)
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    renderer = Renderer()
    renderer.start()
