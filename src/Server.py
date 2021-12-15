"""
This server application was adapted from the solution provided here:
https://github.com/jsantore/ClientServerStart.git

and implements the following additional features:



This modified server application was built by Jacob Bogner and Abe Sabeh
"""
import math
import socket

from arcade import key

import States
import datetime
import arcade
import random
from typing import Dict
import json

SERVER_PORT = 25001

TOTAL_LEVELS = 3
ENEMIES_PER_LEVEL = 3
FRAME_HEIGHT = 90
FRAME_WIDTH = 90
BULLET_SPEED = 5
PLAYER_SPEED = 3
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
MAXBULLETS = 5
W_KEY = '119'
A_KEY = '97'
S_KEY = '115'
D_KEY = '100'

all_players: Dict[str, States.PlayerState] = {}  # key is IP address, value is PlayerState.PlayerState
all_ordnance: list[States.OrdnanceState] = []  # holds all flying projectiles (just bullets rn)

ordnanceCount = 0

def find_ip_address():
    """returns the LAN IP address of the current machine as a string
    A minor revision of this answer:
    https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib#28950776"""
    server_address = ""
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        connection.connect(('10.255.255.255', 1))
        server_address = connection.getsockname()[0]
    except IOError:
        server_address = '127.0.0.1'
    finally:
        connection.close()
    return server_address


def process_player_move(player_move: States.PlayerInput, client_addr: str, gamestate: States.GameState):
    # don't process events too fast, only once every 20 miliseconds
    player_info = gamestate.player_states[client_addr[0]]
    now = datetime.datetime.now()
    if player_info.last_update + datetime.timedelta(milliseconds=20) <= now:
        # if it has been long enough, process movement
        player_info.last_update = now
        delta_x = 0
        delta_y = 0
        # print(player_move.keyPressed)
        if player_move.keyPressed[W_KEY]:
            delta_y = 3
            #print('W')
        elif player_move.keyPressed[S_KEY]:
            delta_y = -3
            #print('S')
        if player_move.keyPressed[A_KEY]:
            delta_x = -3
            #print('A')
        elif player_move.keyPressed[D_KEY]:
            delta_x = 3
            #print('D')
        player_info.x_loc += delta_x
        player_info.y_loc += delta_y
        if player_info.x_loc < 0:
            player_info.x_loc = 20
        elif player_info.x_loc > States.WINDOW_WIDTH:
            player_info.x_loc = States.WINDOW_WIDTH - 20
        if player_info.y_loc < 0:
            player_info.y_loc = 20
        elif player_info.y_loc > States.WINDOW_HEIGHT:
            player_info.y_loc = States.WINDOW_HEIGHT - 20
        if player_move.mousePressed:
            print('New ordnance added')
            newOrdnance = States.OrdnanceState(0, 0, 0, 0, 0)
            newOrdnance.x_loc = player_info.x_loc
            newOrdnance.y_loc = player_info.y_loc

            x_diff = player_move.mouseX - player_info.x_loc
            y_diff = player_move.mouseY - player_info.y_loc

            angle = math.atan2(y_diff, x_diff)
            newOrdnance.angle = math.degrees(angle)
            print(f"Bullet angle: {newOrdnance.angle:.2f}")
            newOrdnance.change_x = math.cos(newOrdnance.angle) * BULLET_SPEED
            newOrdnance.change_y = math.sin(newOrdnance.angle) * BULLET_SPEED
            all_ordnance.append(newOrdnance)
            if len(all_ordnance) > MAXBULLETS:
                all_ordnance.pop(0)
            # check_if_at_target(player_info, gamestate.target, gamestate)




def check_if_at_target(player: States.PlayerState, target: States.EnemyState,
                       gamestate: States.GameState):
    ##cheating a bit here since I'm running out of time. I know player and target are both 72x72 pixals so
    ##I use that shamelessly in this hack.
    playerTopLeft = (player.x_loc - 36, player.y_loc + 36)  # tuple of the top left corner of the player
    playerBottomRight = (player.x_loc + 36, player.y_loc - 36)
    TargetTopLeft = (target.xLoc - 36, target.yloc + 36)
    target_bottom_right = (target.xLoc + 36, target.yloc - 36)
    # Now lets use the good old geeks for geeks method https://www.geeksforgeeks.org/find-two-rectangles-overlap/
    # of course I still have to translate from their (terrible) var names to mine
    # If one rectangle is on left side of other
    if playerTopLeft[0] > target_bottom_right[0] or TargetTopLeft[0] > playerBottomRight[0]:
        return
    # If one rectangle is above other
    if playerTopLeft[1] < target_bottom_right[1] or TargetTopLeft[1] < playerBottomRight[1]:
        return

    ##otherwise there must have been a collision
    print("CHECk SUCEEDED!!!!!!!!!!!!!!!!!!!!!!")
    player.points += 5
    gamestate.target = States.EnemyState(random.randint(36, States.WINDOW_WIDTH - 36),
                                         random.randint(36, States.WINDOW_HEIGHT - 36))


def main():
    enemy: list[States.EnemyState] = []
    enemy.append(States.EnemyState(random.randint(36, States.WINDOW_WIDTH - 36),
                              random.randint(36, States.WINDOW_HEIGHT - 36)))
    gameState = States.GameState(all_players, all_ordnance, enemy)
    server_address = find_ip_address()
    print(f" Server Address is: {server_address}, on prt {SERVER_PORT}")
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((server_address, SERVER_PORT))
    while (True):
        data_packet = UDPServerSocket.recvfrom(1024)
        message = data_packet[0]  # data is first in tuple
        client_addr = data_packet[1]  # client IP is second
        if not client_addr[0] in all_players:  # first time this client connected client_addr is (IP_addr, port) we only care about IP per player
            print("saw it for the first time")
            offset = len(all_players) + 1
            # create new player with x and y positions, 0 points and a last update of now
            new_player: States.PlayerState = States.PlayerState(200 * offset, 200 * offset, 0,
                                                                datetime.datetime.now())
            all_players[client_addr[0]] = new_player
        json_data = json.loads(message)
        player_move: States.PlayerInput = States.PlayerInput(**json_data)  # Load player movement from json data received from client
        process_player_move(player_move, client_addr, gameState)
        #process_ordnance_move(player_move, client_addr, gameState)
        response = gameState.to_json()
        UDPServerSocket.sendto(str.encode(response), client_addr)


if __name__ == '__main__':
    main()
