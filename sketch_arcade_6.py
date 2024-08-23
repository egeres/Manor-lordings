import arcade
import arcade.gui
import arcade.gui.widgets.buttons
import arcade.gui.widgets.layout
import arcade.gui.widgets.text


# Create a window
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(900, 900, "Arcade Button with Panel Example")
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        font_path = "C:/Github/Manor-lordings/art/EXEPixelPerfect.ttf"
        arcade.load_font(font_path)

        # JetBrainsMono-Regular
        font_path_jb = "C:/Github/Manor-lordings/art/F.ttf"
        arcade.load_font(font_path_jb)

        self.v_box = arcade.gui.widgets.layout.UIBoxLayout()
        self.v_box.with_background(
            color=arcade.color.LIGHT_BLUE,
        )
        ui_text_label = arcade.gui.widgets.text.UITextArea(
            text="- Health: 3/3\n- Heal  : 3/3",
            font_size=102,
            height=300,
            width=600,
            font_name="EXEPixelPerfect",
        )
        self.v_box.add(ui_text_label)
        self.v_box.add(
            arcade.gui.UILabel(
                width=300,
                height=300,
                text="- Health: 3/3\n- Heal  : 3/3",
                text_color=arcade.color.BLACK,
                font_size=50,
                font_name="EXEPixelPerfect",
                multiline=True,
            )
        )
        self.v_box.add(
            arcade.gui.UILabel(
                width=300,
                height=300,
                text="- Health: 3/3\n- Heal  : 3/3",
                text_color=arcade.color.BLACK,
                font_size=50,
                font_name="F",
                multiline=True,
            )
        )
        self.ui.add(arcade.gui.widgets.layout.UIAnchorLayout(children=[self.v_box]))

    def on_draw(self):
        self.clear()
        self.ui.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()


if __name__ == "__main__":
    window = MyGame()
    arcade.run()
