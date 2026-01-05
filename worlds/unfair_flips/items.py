from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.unfair_flips import *
from worlds.unfair_flips.data import *
from BaseClasses import Item, ItemClassification, MultiWorld, Location


class UnfairFlipsItem(Item):
    game: str = "Unfair Flips"


def get_random_item_names(rand, k: int, weights: dict[str, int]) -> str:
    random_items = rand.choices(
        list(weights.keys()),
        weights=list(weights.values()),
        k=k)
    return random_items


def create_single(name: str, world: UnfairFlipsWorld, item_class: ItemClassification = None) -> None:
    classification = unfair_flips_item_table[name].classification if item_class is None else item_class
    world.itempool.append(UnfairFlipsItem(name, classification, unfair_flips_item_table[name].code, world.player))


def create_multiple(name: str, amount: int, world: UnfairFlipsWorld, item_class: ItemClassification = None):
    for i in range(amount):
        create_single(name, world, item_class)


def create_items(world: UnfairFlipsWorld):
    total_location_count: int = len(world.multiworld.get_unfilled_locations(world.player))

    # Generic
    gate_count = world.options.required_heads // 2
    create_multiple("Progressive Fairness", gate_count, world)
    create_multiple("Heads+", gate_count, world)
    create_multiple("Flip+", round(gate_count * (1 - JUNK_FACTOR)), world)
    create_multiple("Combo+", round(gate_count * (1 - JUNK_FACTOR)), world)
    create_multiple("Coin+", 4, world)
    create_multiple("AutoFlip+", round(gate_count * (1 - JUNK_FACTOR)), world)

    # Junk
    remaining_locations: int = total_location_count - len(world.itempool)
    trap_count: int = round(remaining_locations * world.options.trap_fill_percentage / 100)
    junk_count: int = remaining_locations - trap_count
    junk = get_random_item_names(world.random, junk_count, junk_weights)
    for name in junk:
        create_single(name, world)
    traps = get_random_item_names(world.random, trap_count, trap_weights)
    for name in traps:
        create_single(name, world)
    world.multiworld.itempool += world.itempool


class ItemData:
    def __init__(self, code: Optional[int], classification: Optional[ItemClassification]):
        self.code = code
        self.classification = classification


unfair_flips_item_table: Dict[str, ItemData] = {
    "Progressive Fairness": ItemData(0x1, ItemClassification.progression),
    "Heads+": ItemData(0x2, ItemClassification.progression_skip_balancing),
    "Flip+": ItemData(0x3, ItemClassification.useful),
    "Combo+": ItemData(0x4, ItemClassification.progression),
    "Coin+": ItemData(0x5, ItemClassification.progression),
    "AutoFlip+": ItemData(0x6, ItemClassification.useful),
    "Tails Trap": ItemData(0x10, ItemClassification.trap),
    "Penny Trap": ItemData(0x11, ItemClassification.trap),
    "Tax Trap": ItemData(0x12, ItemClassification.trap),
    "Slow Trap": ItemData(0x13, ItemClassification.trap),
    "$": ItemData(0x20, ItemClassification.filler),
    "$$": ItemData(0x21, ItemClassification.filler),
    "$$$": ItemData(0x22, ItemClassification.filler),
}


junk_weights = {
    "$": 10,
    "$$": 5,
    "$$$": 1
}


trap_weights = {
    "Tails Trap": 1,
    "Penny Trap": 1,
    "Tax Trap": 1,
    "Slow Trap": 1,
}