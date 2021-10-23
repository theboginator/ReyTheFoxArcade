import arcade
import pathlib

class TiledWindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.map_location = pathlib.Path.cwd()/'Assets'/'world'/'mapdata'/'perkins-cove_L1.json'
        self.map_location2 = pathlib.Path.cwd()/'Assets'/'world'/'mapdata'/'perkins-cove_L2.json'
        self.map_location3 = pathlib.Path.cwd()/'Assets'/'world'/'mapdata'/'perkins-cove_L3.json'
        self.mapscene = None
        self.mapscene2 = None
        self.mapscene3 = None
        self.player = None
        self.player_bullet = None
        self.wall_layer = None
        self.wall_layer2 = None
        self.wall_layer3 = None
        self.player_list = None
        self.collision_engine = None
        self.collision_engine2 = None
        self.collision_engine3 = None
        self.move_speed = 3
        self.health = 100
        self.lives = 3
        self.level1 = 1
        self.level2 = 0
        self.level3 = 0

    def setup(self):
        #Load maps
        sample_map = arcade.tilemap.load_tilemap(self.map_location)
        self.mapscene = arcade.Scene.from_tilemap(sample_map)
        self.wall_layer = sample_map.sprite_lists['WallLayer1']

        sample_map2 = arcade.tilemap.load_tilemap(self.map_location2)
        self.mapscene2 = arcade.Scene.from_tilemap(sample_map2)
        self.wall_layer2 = sample_map2.sprite_lists['WallLayer2']

        sample_map3 = arcade.tilemap.load_tilemap(self.map_location3)
        self.mapscene3 = arcade.Scene.from_tilemap(sample_map3)
        self.wall_layer3 = sample_map3.sprite_lists['WallLayer3']

        #Load the player:
        player_image_file = pathlib.Path.cwd()/'assets'/'player'/'armed_rey.png'
        self.player = arcade.Sprite(player_image_file)
        bullet_image_file = pathlib.Path.cwd()/'assets'/'raw'/'bullet.png'
        self.player_bullet = arcade.Sprite(bullet_image_file)
        self.player.center_x = 300 #special number
        self.player.center_y = 500 #also special number/

        #Define player list:
        self.player_list = arcade.SpriteList()

        self.player_list.append(self.player)


        #Define collisions between player and a wall for all maps
        self.collision_engine = arcade.PhysicsEngineSimple(self.player, self.wall_layer)
        self.collision_engine2 = arcade.PhysicsEngineSimple(self.player, self.wall_layer2)
        self.collision_engine3 = arcade.PhysicsEngineSimple(self.player, self.wall_layer3)
        self.bullet_collision = arcade.PhysicsEngineSimple(self.player_bullet, self.wall_layer)
        self.bullet_collision2 = arcade.PhysicsEngineSimple(self.player_bullet, self.wall_layer2)
        self.bullet_collision3 = arcade.PhysicsEngineSimple(self.player_bullet, self.wall_layer3)

        #self.level1colls = arcade.check_for_collision_with_list(self.player, self.wall_layer)
        self.test = 1

    def on_draw(self):
        arcade.start_render()
        #Draw map:
        self.mapscene.draw()
        #Draw every player in playerlist:
        self.player_list.draw()
        if self.health == 90:
            self.mapscene2.draw()
            self.level1 = 0
            self.level2 = 1
            self.level3 = 0
            self.player_list.draw()
        elif self.health == 80:
            self.mapscene3.draw()
            self.level1 = 0
            self.level2 = 0
            self.level3 = 1
            self.player_list.draw()
        arcade.draw_text(f"Health: {self.health}", 10, 920, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 200, 920, arcade.color.WHITE, 14)

    def on_update(self, delta_time: float):
        # Run collision check

        if self.level1 == 1:
            self.level1colls = arcade.check_for_collision_with_list(self.player, self.wall_layer)
            self.collision_engine.update()
            self.bullet_collision.update()
            if len(self.level1colls) > 0:
                self.lives -= 1


        elif self.level2 == 1:
            self.collision_engine2.update()
            self.bullet_collision2.update()
        elif self.level3 == 1:
            self.collision_engine3.update()
            self.bullet_collision3.update()





    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = self.move_speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -self.move_speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -self.move_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = self.move_speed
        elif key == arcade.key.V:
            self.health -= 10
        elif key == arcade.key.SPACE:
            self.player_bullet.center_x = self.player.center_x
            self.player_bullet.center_y = self.player.center_y
            self.player_list.append(self.player_bullet)
            self.player_bullet.change_x = self.move_speed


    def on_key_release(self, key: int, modifiers: int):
        if self.player.change_y > 0 and (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y = 0
        elif self.player.change_y < 0 and (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y = 0
        elif self.player.change_x < 0 and (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x = 0
        elif self.player.change_x > 0 and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x = 0