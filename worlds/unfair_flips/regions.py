from __future__ import annotations

import math
from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.unfair_flips import *
from worlds.unfair_flips.locations import *
from BaseClasses import Region, Entrance, CollectionState
from worlds.unfair_flips.rules import *


def connect_regions(world: UnfairFlipsWorld, from_name: str, to_name: str, entrance_name: str) -> Entrance:
    entrance_region = world.multiworld.get_region(from_name, world.player)
    exit_region = world.multiworld.get_region(to_name, world.player)
    return entrance_region.connect(exit_region, entrance_name)


def create_region(world: UnfairFlipsWorld, name: str, region_type: str, gate_index=None):
    reg = Region(name, world.player, world.multiworld)
    world.multiworld.regions.append(reg)
    if gate_index is not None:
        if region_type == "Fairness":
            create_heads_count_locations(world, reg, gate_index)
        elif region_type == "Shop":
            create_shop_locations(world, reg, gate_index)


def create_regions(world: UnfairFlipsWorld):
    create_region(world, "Menu", "Menu")
    for gate_index in range(math.ceil(world.options.required_heads / 2)):
        create_region(world, f"Fairness Gate {gate_index + 1}", "Fairness", gate_index)
        create_region(world, f"Shop Gate {gate_index + 1}", "Shop", gate_index)


def connect_all_regions(world: UnfairFlipsWorld):
    coin_value_requirements = 0
    num_gates = math.ceil(world.options.required_heads / 2)

    value_upgrade_gates = {
        round((i + 1) * (num_gates - 1) / 4)
        for i in range(4)
    }

    for gate_index in range(num_gates):
        entrance: Entrance
        if gate_index == 0:
            fairness_entrance = connect_regions(world, "Menu", "Fairness Gate 1", "Menu -> Fairness Gate 1")
            shop_entrance = connect_regions(world, "Fairness Gate 1", "Shop Gate 1", "Fairness Gate 1 -> Shop Gate 1")
        else:
            fairness_entrance = connect_regions(
                world,
                f"Fairness Gate {gate_index}",
                f"Fairness Gate {gate_index + 1}",
                f"Fairness Gate {gate_index} -> Fairness Gate {gate_index + 1}",
            )
            shop_entrance = connect_regions(
                world,
                f"Fairness Gate {gate_index + 1}",
                f"Shop Gate {gate_index + 1}",
                f"Fairness Gate {gate_index + 1} -> Shop Gate {gate_index + 1}",
            )
        fairness_entrance.access_rule = lambda state, gate=gate_index, player=world.player: (
            state.has(f"Progressive Fairness", player, gate) and state.has(f"Heads+", player, max(gate - 1, 0))
        )
        if gate_index in value_upgrade_gates:
            coin_value_requirements += 1
        shop_entrance.access_rule = lambda state, gate=gate_index, player=world.player, value=coin_value_requirements: (
            state.has(f"Combo+", player, max(gate - 1, 0)) and state.has("Coin+", player, value) and state.has(f"Flip+", player, max(gate - 1, 0))
        )

