from __future__ import annotations

from dataclasses import dataclass
from Options import OptionGroup, PerGameCommonOptions
from .option_groups import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import GarfKartWorld


@dataclass
class GarfKartOptions(PerGameCommonOptions):
    # Goal Options
    goal: Goal
    cc_requirement: CCRequirement
    time_trial_goal_grade: TimeTrialGoalGrade

    # Race Randomizer Options
    randomize_races: RandomizeRaces
    progressive_cups: ProgressiveCups
    time_trial_randomization: TimeTrialRandomization

    # Puzzle Piece Options
    randomize_puzzle_pieces: RandomizePuzzlePieces
    puzzle_piece_count: PuzzlePieceCount

    # Character Options
    randomize_characters: RandomizeCharacters
    randomize_karts: RandomizeKarts
    randomize_hats: RandomizeHats
    randomize_spoilers: RandomizeSpoilers
    stat_randomizer: StatRandomizer
    random_stat_values: RandomStatValues

    # Game Options
    single_lap_mode: SingleLapMode
    lap_count: LapCount
    disable_cpu_items: DisableCPUItems
    item_mania: ItemMania
    springs_only: SpringsOnly
    """
    Other game option ideas:
    - cpu_scaling (scales CPU kart speed up/down by a percentage)
    - rubber_banding (scales CPU rubber banding settings to speed them up when they're significantly behind and
        slow them down when they're significantly ahead)
    """


    # Other Randomizer Options
    randomize_items: RandomizeItems
    lap_sanity: LapSanity
    trap_percentage: TrapPercentage
    death_link: DeathLink


option_groups = [
    OptionGroup(
        "Goal Options",
        [Goal, CCRequirement, TimeTrialGoalGrade],
    ),
    OptionGroup(
        "Race Randomizer Options",
        [RandomizeRaces, ProgressiveCups, TimeTrialRandomization],
    ),
    OptionGroup(
        "Puzzle Piece Options",
        [RandomizePuzzlePieces, PuzzlePieceCount]
    ),
    OptionGroup(
        "Character Options",
        [RandomizeCharacters, RandomizeKarts, RandomizeHats, RandomizeSpoilers, StatRandomizer, RandomStatValues]
    ),
    OptionGroup(
        "Game Options",
        [SingleLapMode, LapCount, DisableCPUItems, ItemMania, SpringsOnly],
    ),
    OptionGroup(
        "Other Randomizer Options",
        [RandomizeItems, LapSanity, TrapPercentage, DeathLink],
    ),
]

class RandomizerType:
    not_random = 0
    locations_only = 1
    random = 2

def is_races_randomized(world: GarfKartWorld):
    if world.options.randomize_races in ["races", "cups_and_races"]:
        return RandomizerType.random
    
    if world.options.goal == "races":
        return RandomizerType.locations_only
    
    return RandomizerType.not_random

def is_cups_randomized(world: GarfKartWorld):
    if world.options.randomize_races in ["cups", "cups_and_races"]:
        return RandomizerType.random
    
    if world.options.goal == "grand_prix":
        return RandomizerType.locations_only
    
    return RandomizerType.not_random