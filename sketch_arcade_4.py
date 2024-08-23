import arcade
import arcade.gui

# Create a window
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Arcade Button with Panel Example")
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Create a vertical box to hold the button
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the button to open the panel
        open_panel_button = arcade.gui.UIFlatButton(text="Open Panel", width=200)
        open_panel_button.on_click = self.on_open_panel_button_click

        # Add the button to the layout
        self.v_box.add(open_panel_button)

        # Add the layout to the UIManager anchored to the right side
        self.ui_manager.add(
            # UIAnchorLayout
            arcade.gui.UIAnchorLayout(
                anchor_x="right", anchor_y="center_y", child=self.v_box
            )
        )

        # Create a variable to track if the panel is open
        self.panel_visible = False

        # Create a vertical box for the panel
        self.panel_box = arcade.gui.UIBoxLayout()

        # # Add a "Hello World" label to the panel
        # self.hello_label = arcade.gui.UILabel(text="Hello World", text_color=arcade.color.RED)
        # # Add the label to the panel's layout
        # self.panel_box.add(self.hello_label)

        f = r"C:\Github\Manor-lordings\art\EXEPixelPerfect.ttf"

        font_path = "C:/Github/Manor-lordings/art/EXEPixelPerfect.ttf"
        arcade.load_font(font_path)

        self.hello_label_1 = arcade.gui.UILabel(text="Hello World 1", text_color=arcade.color.RED, font_size=30, font_name="EXEPixelPerfect")
        self.hello_label_2 = arcade.gui.UILabel(text="Hello World 2", text_color=arcade.color.BLUE, font_size=30, font_name="EXEPixelPerfect")
        self.hello_label_3 = arcade.gui.UILabel(text="Hello World 3", text_color=arcade.color.GREEN, font_size=30, font_name="EXEPixelPerfect")
        self.panel_box.add(self.hello_label_1)
        self.panel_box.add(self.hello_label_2)
        self.panel_box.add(self.hello_label_3)
        # self.hello_label_4 = arcade.gui.UILabel(text="- Hello\n- World 3", text_color=arcade.color.BLACK, font_size=30, font_name="EXEPixelPerfect", multiline=True, width=200)
        # self.panel_box.add(self.hello_label_4)
        self.hello_label_4 = arcade.gui.UILabel(
            width=300,
            height=300,
            text="- Hello\n- World 3",
            text_color=arcade.color.BLACK,
            font_size=30,
            font_name="EXEPixelPerfect",
            multiline=True,
            # wrap_lines=False,
            # anchor_x='left',
            # width=200  # Specify the width for wrapping
        )

        # Add the label to the panel's layout
        self.panel_box.add(self.hello_label_4)



        # Create a simple colored background texture for the panel
        background_color = arcade.make_soft_square_texture(256, arcade.color.LIGHT_BLUE, 255, 255)

        # Wrap the panel's content (self.panel_box) in a UITexturePane
        # self.texture_panel = arcade.gui.UITexturePane(
        # self.texture_panel = arcade.gui.UITexturePane(
        # self.texture_panel = arcade.gui.UILayout(
        #     self.panel_box,
        #     tex=background_color,
        #     padding=(10, 10, 10, 10)  # Add some padding inside the panel
        # )

        # Create the panel as a widget, hidden initially by setting anchor outside of the view
        # self.panel = arcade.gui.UIAnchorWidget(
        self.panel = arcade.gui.UIAnchorLayout(
            # anchor_x="right", anchor_y="center_y", child=self.texture_panel, align_x=200
            anchor_x="right", anchor_y="center_y", child=self.panel_box, align_x=200
        )

        # Add the panel to the UIManager, but it starts off hidden
        self.ui_manager.add(self.panel)

    def on_open_panel_button_click(self, event):
        # Toggle the visibility of the panel
        if not self.panel_visible:
            self.panel.align_x = -500  # Move the panel into view

            self.panel_visible = True
        else:
            self.panel.align_x = 200  # Hide the panel by moving it out of view
            self.panel_visible = False

        # Ensure UIManager updates its layout
        # self.ui_manager.do_layout()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()


# Run the game
if __name__ == "__main__":
    window = MyGame()
    arcade.run()
