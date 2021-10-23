import arcade
import pathlib

TOTAL_LEVELS = 3


class TiledWindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'world' / 'mapdata' / 'perkins-cove_L1.json'
        self.map_location2 = pathlib.Path.cwd() / 'Assets' / 'world' / 'mapdata' / 'perkins-cove_L2.json'
        self.map_location3 = pathlib.Path.cwd() / 'Assets' / 'world' / 'mapdata' / 'perkins-cove_L3.json'
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
        self.map_list = []
        self.wall_list = []
        self.playerCollisionEngineArray = []
        self.bulletCollisionEngineArray = []
        self.move_speed = 3
        self.health = 100
        # TEST:
        self.activeLevel = 1
        self.totalLevels = 3

        self.lives = 3
        self.level1 = 1
        self.level2 = 0
        self.level3 = 0

    def setup(self):
        # Load maps and an array of enemies for each map
        sample_map = arcade.tilemap.load_tilemap(self.map_location)
        self.mapscene = arcade.Scene.from_tilemap(sample_map)
        self.wall_layer = sample_map.sprite_lists['WallLayer1']

        self.map_list.append(self.mapscene)
        self.wall_list.append(self.wall_layer)

        sample_map2 = arcade.tilemap.load_tilemap(self.map_location2)
        self.mapscene2 = arcade.Scene.from_tilemap(sample_map2)
        self.wall_layer2 = sample_map2.sprite_lists['WallLayer2']

        self.map_list.append(self.mapscene2)
        self.wall_list.append(self.wall_layer2)

        sample_map3 = arcade.tilemap.load_tilemap(self.map_location3)
        self.mapscene3 = arcade.Scene.from_tilemap(sample_map3)
        self.wall_layer3 = sample_map3.sprite_lists['WallLayer3']

        self.map_list.append(self.mapscene3)
        self.wall_list.append(self.wall_layer3)

        # Load the player:
        player_image_file = pathlib.Path.cwd() / 'assets' / 'player' / 'armed_rey.png'
        self.player = arcade.Sprite(player_image_file)
        bullet_image_file = pathlib.Path.cwd() / 'assets' / 'raw' / 'bullet.png'
        self.player_bullet = arcade.Sprite(bullet_image_file)
        self.player.center_x = 300  # special number
        self.player.center_y = 500  # also special number/

        # Define player list:
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Define collisions between player and a wall for all maps
        ctr = 0
        while ctr < self.totalLevels:
            print('Setup level ', ctr)
            currentWallLayer = self.wall_list[ctr]
            self.playerCollisionEngineArray.append(arcade.PhysicsEngineSimple(self.player, currentWallLayer))
            self.bulletCollisionEngineArray.append(arcade.PhysicsEngineSimple(self.player_bullet, self.wall_list[ctr]))
            ctr += 1
        self.collision_engine = arcade.PhysicsEngineSimple(self.player, self.wall_layer)
        self.test = 1

    def on_draw(self):
        arcade.start_render()
        # Draw map:
        self.map_list[self.activeLevel].draw()
        self.player_list.draw()
        arcade.draw_text(f"Health: {self.health}", 10, 920, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 200, 920, arcade.color.WHITE, 14)

    def on_update(self, delta_time: float):
        # Run collision check
        self.newCollisions = arcade.check_for_collision_with_list(self.player, self.wall_list[self.activeLevel])
        self.playerCollisionEngineArray[self.activeLevel].update()
        self.bulletCollisionEngineArray[self.activeLevel].update()

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
