from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions
from worlds.unfair_flips.data import *


class RequiredHeads(Range):
    """
    Number of heads in a row needed to goal
    """
    display_name = "Required Heads"
    range_start = 10
    range_end = MAX_HEADS
    default = 15

class AutoFlip(Toggle):
    """
    Adds autoflip upgrades to the pool and enables the autoflip button in game
    """
    display_name = "AutoFlip"


class TrapFillPercentage(Range):
    """
    The percentage of filler that will be replaced by traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class StartingHeadsChance(Range):
    """
    The initial chance for the coin to land on heads without any upgrades
    """
    display_name = "Starting Heads Chance"
    range_start = 10
    range_end = 20
    default = 15


class FlipDifficulty(Range):
    """
    How many flips logic expects you to do to buy an item in the shop
    """
    display_name = "Flip Difficulty"
    range_start = 20
    range_end = 50
    default = 30


class DeathLinkChance(Range):
    """
    Percentage chance to send a death on breaking a streak of heads
    """
    display_name = "Death Link Chance"
    range_start = 1
    range_end = 10
    default = 5


class DeathLinkMinStreak(Range):
    """
    Minimum streak of heads required for death to send when broken
    """
    display_name = "Death Link Minimum Streak"
    range_start = 4
    range_end = MAX_HEADS - 1
    default = 5


# class EnergyLink(Toggle):
#     """
#     Send excess money beyond the cap to the energy pool
#     """
#     display_name = "Energy Link"


unfair_flips_options = [
    OptionGroup("Goal Options", [
        RequiredHeads,
        StartingHeadsChance
    ]),
    OptionGroup("Logic Options", [
        AutoFlip
    ]),
    OptionGroup("Traps", [
        TrapFillPercentage
    ]),
    # OptionGroup("Energy Link", [
    #     EnergyLink
    # ]),
    OptionGroup("Death Link", [
        DeathLink,
        DeathLinkMinStreak,
        DeathLinkChance
    ]),
]


@dataclass
class UnfairFlipsOptions(PerGameCommonOptions):
    required_heads: RequiredHeads
    starting_heads_chance: StartingHeadsChance
    auto_flip: AutoFlip
    trap_fill_percentage: TrapFillPercentage
    flip_difficulty: FlipDifficulty
    # energy_link: EnergyLink
    death_link: DeathLink
    death_link_min_streak: DeathLinkMinStreak
    death_link_chance: DeathLinkChance

