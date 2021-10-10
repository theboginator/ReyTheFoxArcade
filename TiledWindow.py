import arcade
import pathlib


class TiledWindow (arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Initial Tiled Map Super Simple Example")
        self.map_location = pathlib.Path.cwd()/'Assets'/'gradmap.json'
        self.mapscene = None
        self.player = None
        self.wall_layer = None
        self.player_list = None
        self.collision_engine = None
        self.move_speed = 3

    def setup(self):
        sample__map = arcade.tilemap.load_tilemap(self.map_location)
        self.mapscene = arcade.Scene.from_tilemap(sample__map)
        player_image_file = pathlib.Path.cwd()/'assets'/'orc2.png'
        self.player = arcade.Sprite(player_image_file)
        self.player.center_x = 96 #special number
        self.player.center_y = 224 #also special number
        self.wall_layer = sample__map.sprite_lists['WallLayer']
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.collision_engine = arcade.PhysicsEngineSimple(self.player, self.wall_layer)

    def on_draw(self):
        arcade.start_render()
        self.mapscene.draw()
        self.player_list.draw()

    def on_update(self, delta_time: float):
        self.collision_engine.update()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.W:
            self.player.change_y = self.move_speed
        elif key == arcade.key.S:
            self.player.change_y = -self.move_speed
        elif key == arcade.key.A:
            self.player.change_x = -self.move_speed
        elif key == arcade.key.D:
            self.player.change_x = self.move_speed

    def on_key_release(self, key: int, modifiers: int):
        if self.player.change_y > 0 and key == arcade.key.W:
            self.player.change_y = 0
        elif self.player.change_y < 0 and key == arcade.key.S:
            self.player.change_y = 0
        elif self.player.change_x < 0 and key == arcade.key.A:
            self.player.change_x = 0
        elif self.player.change_x > 0 and key == arcade.key.D:
            self.player.change_x = 0