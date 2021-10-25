import arcade
import pathlib
from typing import get_type_hints, List

FRAME_HEIGHT = 512
FRAME_WIDTH = 512

class AnimatedSpriteWindow(arcade.Window):
    def __init__ (self):
        super().__init__()
        self.coin = None
        self.thing_list = None

    def setup(self):
        coin_path = pathlib.Path.cwd()/'assets'/'Coin_Spin_Animation_A.png'
        self.coin_sprite = \
            arcade.AnimatedTimeBasedSprite(coin_path, 0.5, center_x=300, center_y=300)
        coin_frames: List[arcade.AnimationKeyframe] = []
        for row in range(4):
            for col in range(4):
                frame = \
                    arcade.AnimationKeyframe(col*row, 100, arcade.load_texture(str(coin_path), x=col*FRAME_WIDTH, y=row*FRAME_HEIGHT, width=FRAME_WIDTH, height=FRAME_HEIGHT))
                coin_frames.append(frame)
            self.coin_sprite.frames = coin_frames
            self.thing_list = arcade.SpriteList()
            self.thing_list.append(self.coin_sprite)

    def update(self, delta_time: float):
        self.coin_sprite.update_animation()

    def on_draw(self):
        arcade.start_render()
        self.thing_list.draw()

def main():
    game_window = AnimatedSpriteWindow()
    game_window.setup()
    arcade.run()

if __name__ == '__main__':
    main()