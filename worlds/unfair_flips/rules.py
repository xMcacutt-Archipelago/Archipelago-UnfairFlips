from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.unfair_flips import *
import math
import random

from worlds.unfair_flips import *


coin_values = [1, 5, 10, 25, 100]


def can_practically_get_heads_in_a_row(world, heads_upgrade_count, heads_count):
    heads_chance = get_heads_chance(world, heads_upgrade_count)
    return heads_chance ** heads_count > PRACTICALITY_THRESHOLD

def get_heads_chance(world: UnfairFlipsWorld, heads_items):
    total_heads_items = world.options.required_heads // 2
    MIN_HEADS_CHANCE = world.options.starting_heads_chance.value / 100
    return MIN_HEADS_CHANCE + (((MAX_HEADS_CHANCE - MIN_HEADS_CHANCE) / total_heads_items) * heads_items)