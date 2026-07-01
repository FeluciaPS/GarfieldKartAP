from __future__ import annotations

from dataclasses import dataclass
from Options import Choice

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..world import GarfKartWorld


class Goal(Choice):
    """
    Determines what your goal is to consider the game beaten.

    - Grand Prix: Get first place in every grand prix cup
    - Races: Get first place in every race
    - Time Trials: Gain medals in all time trials
    - Puzzle Piece Hunt: Collect specified amount of puzzle pieces
    """
    display_name = "Goal"

    default = 1
    option_grand_prix = 0
    option_races = 1
    option_time_trials = 2
    option_puzzle_piece_hunt = 3

class CCRequirement(Choice):
    """
    Sets the CC you will be expected to play on. This determines checks added for winning on specific CCs,
    as well as what you need to be able to goal with grand_prix and races on. Selecting any allows winning
    on any CC of your choice, with no extra cc checks added.

    Winning on 150cc will send all checks for 50 and 100cc, and same goes for 100cc giving 50cc checks.
    For goaling your slot, if the option is not set to grand prix or races, this option just affects the extra cc win checks.
    """
    display_name = "CC Requirement"

    default = 0
    option_any = 0
    option_50cc = 1
    option_100cc = 2
    option_150cc = 3

class TimeTrialGoalGrade(Choice):
    """
    Sets the minimum medal grade required for the Time Trials goal
    !!!IMPORTANT!!! Platinum medals require certain kart combinations to be
    reasonably achievable. These aren't implemented in logic yet, so randomizing
    kart loadouts may lead to impossible games.

    If the goal is not Time Trials, this option does nothing.
    """
    display_name = "Time Trials Goal Grade"

    default = 1
    option_bronze = 0
    option_silver = 1
    option_gold = 2
    option_platinum = 3