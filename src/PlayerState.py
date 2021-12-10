import datetime
from dataclasses import dataclass
from typing import Dict

import arcade
import json
from dataclasses_json import dataclass_json

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


# a major breakthrough was to find the dataclasses_json package which automatically converted between json and
# dataclasses. My commented out methods worked fine for individual atomic types, but it fell apart for lists
# and other collection types as instance variables in the data classes. using the @dataclass took care of that.

@dataclass_json
@dataclass
class PlayerState:  #Contains data about the player
    x_loc: int
    y_loc: int
    level: int      #Will allow us to tell what level the player is on
    points: int
    last_update: datetime.datetime

@dataclass_json
@dataclass
class TargetState: #Add enemy state classes here probably
    xLoc: int
    yloc: int



@dataclass
class PlayerMovement:
    keys = {
        arcade.key.UP: False,
        arcade.key.DOWN: False,
        arcade.key.LEFT: False,
        arcade.key.RIGHT: False}
    # to string is purely for debugging
    def __str__(self):
        return f"UP: {self.keys[arcade.key.UP]}, Down: {self.keys[arcade.key.DOWN]}, Left: {self.keys[arcade.key.LEFT]}, Right: {self.keys[arcade.key.RIGHT]}, "


@dataclass_json
@dataclass
class GameState:
    player_states: Dict[str, PlayerState]
    target: TargetState