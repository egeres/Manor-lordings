import arcade
import arcade.gl
from pyglet.math import Vec2


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 800)
        self.a = arcade.SpriteList()
        s = arcade.Sprite("grass_dark_0.png")
        s.center_x = 0
        s.center_y = 0
        self.a.append(s)
        # s = arcade.Sprite("grass_light_0.png")
        # s.center_x = 16
        # s.center_y = 1
        # self.a.append(s)
        self.camera = arcade.Camera2D(zoom=50)
        self.camera.bottom_left = Vec2(0, 0)
    def on_draw(self):
        self.clear()
        self.camera.use()
        # self.s.draw()
        self.a.draw(pixelated=True)
if __name__ == "__main__":
    window = MyGame()
    arcade.run()


# import arcade
# class MyGame(arcade.Window):
#     def __init__(self):
#         super().__init__(800, 800)
#         self.a = arcade.SpriteList()
#         self.a.append(
#             arcade.Sprite(
#                 "grass_dark_0.png",
#                 scale=40,
#                 center_x=self.width // 2,
#                 center_y=self.height // 2,
#             )
#         )
#         self.camera = arcade.Camera2D()
#     def on_draw(self):
#         self.clear()
#         self.camera.use()
#         self.a.draw(pixelated=True)
# if __name__ == "__main__":
#     window = MyGame()
#     arcade.run()


# class MyGame(arcade.Window):
#     def __init__(self):
#         super().__init__(800, 800)
#         self.a = arcade.SpriteList()
#         self.a.append(
#             arcade.Sprite(
#                 "grass_dark_0.png",
#                 scale=40,
#                 center_x=self.width // 2,
#                 center_y=self.height // 2,
#             )
#         )
#         self.camera = arcade.Camera2D()

#     def on_draw(self):
#         self.clear()
#         self.camera.use()
#         self.a.draw(pixelated=True)


# if __name__ == "__main__":
#     window = MyGame()
#     arcade.run()
