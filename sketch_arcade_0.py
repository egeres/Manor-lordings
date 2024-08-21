# conda install -c conda-forge libstdcxx-ng -y
# For WSL
# https://github.com/microsoft/WSL/issues/2855
#
# sudo apt update
# sudo apt install mesa-utils
# export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
# glxgears

import arcade
import arcade.gui


# Create a window
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Arcade Button Example")
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Create a vertical box to hold the buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create a button
        my_button = arcade.gui.UIFlatButton(text="Click Me", width=200)
        my_button.on_click = (
            self.on_button_click
        )  # Set what happens when button is clicked

        # Add the button to the layout
        self.v_box.add(my_button)

        # Add the layout to the UIManager
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_button_click(self, event):
        print("Button clicked!")

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
