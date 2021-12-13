import datetime
from dataclasses import dataclass
from typing import Dict

import arcade
import json
from dataclasses_json import dataclass_json

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960


# a major breakthrough was to find the dataclasses_json package which automatically converted between json and
# dataclasses. My commented out methods worked fine for individual atomic types, but it fell apart for lists
# and other collection types as instance variables in the data classes. using the @dataclass took care of that.

@dataclass_json
@dataclass
class PlayerState:  # Contains data about a player
    x_loc: int
    y_loc: int
    # level: int      #Will allow us to tell what level the player is on
    points: int
    last_update: datetime.datetime


@dataclass_json
@dataclass
class EnemyState:  # Add enemy state classes here probably
    xLoc: int
    yloc: int


@dataclass_json
@dataclass
class OrdnanceState:  # Data about ordnance
    x_loc: int
    y_loc: int
    angle: float

@dataclass_json
@dataclass
class PlayerInput:
    keyPressed: dict[arcade.key, bool]
    mousePressed: bool
    mouseX: float
    mouseY: float
    """
    keys = {
        arcade.key.W: bool,
        arcade.key.A: bool,
        arcade.key.S: bool,
        arcade.key.D: bool,
        arcade.key.UP: bool,
        arcade.key.DOWN: bool,
        arcade.key.LEFT: bool,
        arcade.key.RIGHT: bool
    }
    """


@dataclass_json
@dataclass
class GameState:
    player_states: Dict[str, PlayerState]
    ordnance_state: Dict[int, OrdnanceState]
    enemy_states: EnemyState
