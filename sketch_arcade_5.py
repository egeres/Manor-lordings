import arcade
import arcade.gui








from dataclasses import dataclass
from arcade.gui import UIStyledWidget, UIInteractiveWidget, UIWidget, UIStyleBase


bg_color = arcade.color.GREEN

class MyColorBox(UIStyledWidget, UIInteractiveWidget, UIWidget):
    """
    A colored box, which changes on mouse interaction
    """

    # create the style class, which will be used to define style for any widget state
    @dataclass
    class UIStyle(UIStyleBase):
        color = arcade.color.GREEN


    DEFAULT_STYLE = {
        "normal": UIStyle(),
        "hover": UIStyle(color=arcade.color.YELLOW),
        "press": UIStyle(color=arcade.color.RED),
        "disabled": UIStyle(color=arcade.color.GRAY)
    }

    def get_current_state(self) -> str:
        """Returns the current state of the widget i.e disabled, press, hover or normal."""
        if self.disabled:
            return "disabled"
        elif self.pressed:
            return "press"
        elif self.hovered:
            return "hover"
        else:
            return "normal"

    def do_render(self, surface):
        self.prepare_render(surface)

        # get current style
        style: MyColorBox.UIStyle = self.get_current_style()

        # Get color from current style, it is a good habit to be
        # bullet proven for missing values in case a dict is provided instead of a UIStyle
        color = style.get("color", MyColorBox.UIStyle.bg)

        # render
        if color: # support for not setting a color at all
            surface.clear(bg_color)



# Create a window
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Arcade Button with Panel Example")
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        font_path = "C:/Github/Manor-lordings/art/EXEPixelPerfect.ttf"
        arcade.load_font(font_path)

        open_panel_button = arcade.gui.UIFlatButton(text="Button", width=200)

        # 🥦 0
        # self.ui_manager.add(open_panel_button)

        # 🍅 1
        # self.ui_manager.add(
        #     arcade.gui.UIAnchorLayout(
        #         anchor_x="left", anchor_y="bottom", child=open_panel_button,
        #         width=200,
        #         height=200,
        #     )
        # )

        # 🥦 2
        v_box = arcade.gui.UIBoxLayout(
            style={
                "_bg": arcade.color.GREEN,
                "bg": arcade.color.GREEN,
                "padding": 10,
                "spacing": 10,
            }
        )
        v_box.add(open_panel_button)
        v_box.add(arcade.gui.UILabel(text="AAAA", text_color=arcade.color.RED))
        self.ui_manager.add(v_box)

        # 🧇 3
        # v_box = arcade.gui.UIBoxLayout()
        # v_box.add(open_panel_button)
        # v_box.add(arcade.gui.UILabel(text="AAAA", text_color=arcade.color.RED))
        # self.ui_manager.add(
        #     arcade.gui.UIAnchorLayout(
        #         children=(v_box),
        #         anchor_x="left",
        #         anchor_y="bottom",
        #         heigh=300,
        #         # align_x=20,
        #     )
        # )

        # self.box_0 = arcade.gui.UIBoxLayout()
        # self.box_0.add(open_panel_button)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()


if __name__ == "__main__":
    window = MyGame()
    arcade.run()
