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


def is_shop_accessible(world, heads_upgrade_count, combo_upgrade_count, value_upgrade_count, shop_level, fairness_level):
    item_cost = 10 ** shop_level * 0.9
    capped_value_count = min(value_upgrade_count, len(coin_values) - 1)
    money = simulate_money(
        world,
        get_heads_chance(world, heads_upgrade_count),
        get_combo(world, combo_upgrade_count),
        coin_values[capped_value_count],
        1 + fairness_level * 2,
        10 ** (fairness_level + 1)
    )
    return money > item_cost


# AVERAGE_NUM = 1000
# def simulate_money(
#     world, heads_chance: float, combo: float, coin_value: float, max_combo_length: int, cap: int
# ) -> float:
#     rng = random.Random(8750)
#     flip_difficulty = world.options.flip_difficulty.value
#     total = 0.0
#     for _ in range(AVERAGE_NUM):
#         flip_len = 0
#         money = 0.0
#         for _ in range(flip_difficulty):
#             if rng.random() < heads_chance and flip_len < max_combo_length:
#                 money += combo**flip_len
#                 flip_len += 1
#             else:
#                 flip_len = 0
#         else:
#             flip_len = 0
#         total += money
#     return min(total/AVERAGE_NUM * coin_value, cap)


def get_combo(world, combo_items):
    total_combo_items = round(world.options.required_heads // 2 * (1 - JUNK_FACTOR))
    return MIN_COMBO + (((MAX_COMBO - MIN_COMBO) / total_combo_items) * combo_items)


def get_heads_chance(world: UnfairFlipsWorld, heads_items):
    total_heads_items = world.options.required_heads // 2
    MIN_HEADS_CHANCE = world.options.starting_heads_chance.value / 100
    return MIN_HEADS_CHANCE + (((MAX_HEADS_CHANCE - MIN_HEADS_CHANCE) / total_heads_items) * heads_items)


def simulate_money(world, heads_chance: float, combo: float, coin_value: float, max_combo_length: int, cap: int) -> float:
    flip_difficulty = world.options.flip_difficulty.value
    if heads_chance <= 0 or max_combo_length <= 0:
        return 0.0
    money_per_flip = 0.0
    for i in range(max_combo_length):
        prob_of_streak = heads_chance ** (i + 1)
        money_per_flip += prob_of_streak * (combo ** i)
    total_money = flip_difficulty * money_per_flip * coin_value
    return min(total_money, cap)
