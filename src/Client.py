import asyncio
import json
import math
import pathlib
import socket
import threading

import arcade
import Instruction
import Window
import Server
from src import PlayerState


TOTAL_LEVELS = 3
ENEMIES_PER_LEVEL = 3
FRAME_HEIGHT = 90
FRAME_WIDTH = 90
BULLET_SPEED = 5
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960

client_address = ""
server_address = ""

class BeginGameView(arcade.View):
    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        launch_screen_img = pathlib.Path.cwd()/'assets'/'world'/'launch_screen_detailed.png'
        self.texture = arcade.load_texture(launch_screen_img)
        print("Loading launch screen.")
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        print("Game starting")
        game_view = Window.TiledWindow()
        game_view.setup()
        self.window.show_view(game_view)

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

class TiledWindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.ip_addr = client_address
        self.server_add = server_address
        self.window.set_mouse_visible(True)
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'world' / 'mapdata' / 'perkins-cove_L1.json'
        self.map_location2 = pathlib.Path.cwd() / 'Assets' / 'world' / 'mapdata' / 'perkins-cove_L2.json'
        self.map_location3 = pathlib.Path.cwd() / 'Assets' / 'world' / 'mapdata' / 'perkins-cove_L3.json'
        self.mapscene = None
        self.mapscene2 = None
        self.mapscene3 = None
        self.player = None
        self.enemy = None
        self.player_bullet = None
        self.wall_layer = None
        self.wall_layer2 = None
        self.wall_layer3 = None
        self.player_list = None
        self.collision_engine = None
        self.collision_engine2 = None
        self.collision_engine3 = None
        self.bulletCollisionEngine = None
        self.map_list = []
        self.wall_list = []
        self.enemy_list = []
        # self.bullet_enemy_list = []
        self.playerCollisionEngineArray = []
        self.bulletCollisionEngineArray = []
        self.itemCollisionEngineArray = []
        self.enemyCollisionEngineArray = []
        self.move_speed = 3
        self.score = 0
        # TEST:
        self.activeLevel = 0
        self.totalLevels = 3
        self.totalenemies = 12

        self.lives = 3
        self.level1 = 1
        self.level2 = 0
        self.level3 = 0
        self.fire = 0
        self.mouse = 1

    def setup(self):
        coin_path = pathlib.Path.cwd() / 'assets' / 'Coin_Spin_Animation_A.png'
        self.coin_sprite = \
            arcade.AnimatedTimeBasedSprite(coin_path, 0.5, center_x=400, center_y=830)
        coin_frames: List[arcade.AnimationKeyframe] = []
        for row in range(4):
            for col in range(4):
                frame = \
                    arcade.AnimationKeyframe(col * row, 100, arcade.load_texture(str(coin_path), x=col * FRAME_WIDTH,
                                                                                 y=row * FRAME_HEIGHT,
                                                                                 width=FRAME_WIDTH,
                                                                                 height=FRAME_HEIGHT))
                coin_frames.append(frame)
            self.coin_sprite.frames = coin_frames
            self.thing_list = arcade.SpriteList()
            self.thing_list.append(self.coin_sprite)

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
        self.player.center_x = 300  # special number
        self.player.center_y = 500  # also special number/

        # Define player, enemy, and ordnance lists:
        self.player_list = arcade.SpriteList()
        self.bullet_enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # Put player into player list:
        self.player_list.append(self.player)

        # set up sound for bullet shot
        shot_sound_path = pathlib.Path.cwd() / 'Assets' / "gunshot.mp3"
        self.shot_sound = arcade.load_sound(shot_sound_path)

        x = 0
        y = 0
        while x < 6:
            enemy_image_file = pathlib.Path.cwd() / 'assets' / 'enemy' / 'neckbeard.png'
            enemy = arcade.Sprite(enemy_image_file)
            enemy.center_x = random.randint(100, 900)
            enemy.center_y = random.randint(100, 900)
            self.bullet_enemy_list.append(enemy)
            x += 1

        lvl = 1
        while lvl <= TOTAL_LEVELS:
            self.tempEnemyList = arcade.SpriteList()
            numen = 0
            while numen < ENEMIES_PER_LEVEL * lvl:
                print('put enemy in ', lvl, ' ', numen)
                enemy_image_file = pathlib.Path.cwd() / 'assets' / 'enemy' / 'blue_goon.png'
                enemy = arcade.Sprite(enemy_image_file)
                enemy.center_x = random.randint(100, 900)
                enemy.center_y = random.randint(100, 900)
                self.tempEnemyList.append(enemy)
                numen += 1
            self.enemy_list.append(self.tempEnemyList)
            lvl += 1

        # Define collisions between player and a wall for all maps and enemies
        ctr = 0
        while ctr < self.totalLevels:
            print('Setup level ', ctr)
            currentWallLayer = self.wall_list[ctr]
            self.playerCollisionEngineArray.append(arcade.PhysicsEngineSimple(self.player, currentWallLayer))
            # self.bulletCollisionEngineArray.append(arcade.PhysicsEngineSimple(self.player_bullet_list, self.wall_list[ctr]))
            ctr += 1
        self.collision_engine = arcade.PhysicsEngineSimple(self.player, self.wall_layer)
        self.coincollision_engine = arcade.PhysicsEngineSimple(self.coin_sprite, self.wall_layer)

        lvl = 0
        while lvl < TOTAL_LEVELS:
            ctr = 0
            while ctr < len(self.enemy_list):
                print('pass ', lvl, ' ', ctr)
                self.enemyCollisionEngineArray.append(
                    arcade.PhysicsEngineSimple(self.enemy_list[lvl][ctr], self.wall_list[ctr]))
                ctr += 1
            lvl += 1

    def on_draw(self):
        arcade.start_render()
        # Draw map:
        self.map_list[self.activeLevel].draw()
        self.player_list.draw()
        self.player_bullet_list.draw()
        self.thing_list.draw()
        # self.bullet_enemy_list.draw()
        # self.enemy_list.draw()
        self.enemy_list[self.activeLevel].draw()

        arcade.draw_text(f"Score: {self.score}", 10, 920, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 200, 920, arcade.color.WHITE, 14)

    def on_update(self, delta_time: float):
        # Run collision checks
        self.coin_sprite.update_animation()
        self.wallCollisions = arcade.check_for_collision_with_list(self.player, self.wall_list[self.activeLevel])
        self.enemyCollisions = arcade.check_for_collision_with_list(self.player, self.enemy_list[self.activeLevel])
        self.coincollision_engine.update()  # Change this to array as other engines are
        self.enemyCollisionEngineArray[self.activeLevel].update()
        #check if a bullet has collided with an enemy. If it has, increase the player's score and remove the enemy and bullet
        collisions = [impact for impact in self.enemy_list[self.activeLevel]
                      if arcade.check_for_collision_with_list(impact, self.player_bullet_list)]

        dead_bullets = [impact for impact in self.player_bullet_list
                        if arcade.check_for_collision_with_list(impact, self.enemy_list[self.activeLevel])]

        coin_hits = [impact for impact in self.thing_list
                     if arcade.check_for_collision_with_list(impact, self.player_bullet_list)]

        #wall_bullets = [impact for impact in self.player_bullet_list
        #if arcade.check_for_collision_with_list(impact, self.wall_list[self.activeLevel])]

        if collisions:
            self.score += len(collisions)*5
            eliminations = filter(lambda enemy: enemy in collisions, self.enemy_list[self.activeLevel])
            for enemy in eliminations:
                self.enemy_list[self.activeLevel].remove(enemy)
                print('Enemies left on this level: ', len(self.enemy_list[self.activeLevel]))

        if dead_bullets:
            #self.score += len(collisions)
            eliminations = filter(lambda bullet: bullet in dead_bullets, self.player_bullet_list)
            for bullet in eliminations:
                self.player_bullet_list.remove(bullet)

        # if wall_bullets:
        #     # self.score += len(collisions)
        #     eliminations = filter(lambda bullet: bullet in wall_bullets, self.player_bullet_list)
        #     for bullet in eliminations:
        #         self.player_bullet_list.remove(bullet)

        if coin_hits:
            self.lives += len(coin_hits)
            eliminations = filter(lambda coin: coin in coin_hits, self.thing_list)
            for coin in eliminations:
                self.thing_list.remove(coin)

        if len(self.wallCollisions) > 0 or len(self.enemyCollisions) > 0:
            self.lives -= 1
        #
        if self.fire == 1:
            arcade.play_sound(self.shot_sound)
            self.fire = 0
            # self.bulletCollisionEngine.update()

        self.playerCollisionEngineArray[self.activeLevel].update()
        self.player_bullet_list.update()
        for x in self.enemy_list[self.activeLevel]:
            if x.center_x > self.player.center_x and x.center_y > self.player.center_y:
                x.center_x = x.center_x - 0.5
                x.center_y = x.center_y - 0.5
            elif x.center_x > self.player.center_x and x.center_y < self.player.center_y:
                x.center_x = x.center_x - 0.5
                x.center_y = x.center_y + 0.5
            elif x.center_x < self.player.center_x and x.center_y > self.player.center_y:
                x.center_x = x.center_x + 0.5
                x.center_y = x.center_y - 0.5
            elif x.center_x < self.player.center_x and x.center_y < self.player.center_y:
                x.center_x = x.center_x + 0.5
                x.center_y = x.center_y + 0.5


        if len(self.enemy_list[self.activeLevel]) == 0:
            self.activeLevel += 1
            print('level ', self.activeLevel)
        if self.activeLevel >= TOTAL_LEVELS:
            print('you win')
            view = GameOverView()
            self.window.show_view(view)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = self.move_speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -self.move_speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -self.move_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = self.move_speed
        elif key == arcade.key.V and self.activeLevel + 1 < TOTAL_LEVELS:
            self.activeLevel += 1

    def on_key_release(self, key: int, modifiers: int):
        if self.player.change_y > 0 and (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y = 0
        elif self.player.change_y < 0 and (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y = 0
        elif self.player.change_x < 0 and (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x = 0
        elif self.player.change_x > 0 and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        ##Load in a bullet, give it a firing angle, and push it into the list of active player ordnance
        bullet_image_file = pathlib.Path.cwd() / 'assets' / 'raw' / 'bullet.png'
        new_bullet = arcade.Sprite(bullet_image_file)
        new_bullet.center_x = self.player.center_x
        new_bullet.center_y = self.player.center_y

        x_diff = x - self.player.center_x
        y_diff = y - self.player.center_y

        angle = math.atan2(y_diff, x_diff)
        new_bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {new_bullet.angle:.2f}")

        new_bullet.change_x = math.cos(angle) * BULLET_SPEED
        new_bullet.change_y = math.sin(angle) * BULLET_SPEED

        self.player_bullet_list.append(new_bullet)
        # self.bulletCollisionEngine = arcade.PhysicsEngineSimple(self.player_bullet_list[self.mouse], self.wall_list[1])
        self.fire = 1  # indicator for sound to play


def setup_client_connection(client: TiledWindow):
    client_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_event_loop)
    client_event_loop.create_task(communication_with_server(client, client_event_loop))
    client_event_loop.run_forever()


async  def communication_with_server(client: TiledWindow, event_loop):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while True:
        keystate = json.dumps(client.actions.keys)
        UDPClientSocket.sendto(str.encode(keystate), (client.server_address, Server.SERVER_PORT))
        data_packet = UDPClientSocket.recvfrom(1024)
        data = data_packet[0]  # get the encoded string
        decoded_data: PlayerState.GameState = PlayerState.GameState.from_json(data)
        player_dict = decoded_data.player_states
        target: PlayerState.TargetState = decoded_data.target
        client.target.center_x = target.xLoc
        client.target.center_y = target.yloc
        player_info: PlayerState.PlayerState = player_dict[client.ip_addr]
        client.from_server = player_info.points
        client.player.center_x = player_info.x_loc
        client.player.center_y = player_info.y_loc


def main():
    client_address = Server.find_ip_address()
    server_address = input("Enter server IP: ")
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Captain Neckbeard: Perkins Cove")
    #Load launch screen:
    start_view = Instruction.BeginGameView()
    window.show_view(start_view)
    #begin:
    arcade.run()
    client_thread = threading.Thread(target=setup_client_connection, args=(window,), daemon=True)
    client_thread.start()
    arcade.run()

if __name__ == '__main__':
    main()