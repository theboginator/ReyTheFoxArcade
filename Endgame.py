import pathlib
import arcade
import Window

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        launch_screen_img = pathlib.Path.cwd()/'assets'/'world'/'end_screen_detailed.png'
        self.texture = arcade.load_texture(launch_screen_img)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        print("Game starting")
        game_view = Window.TiledWindow()
        game_view.setup()
        self.window.show_view(game_view)