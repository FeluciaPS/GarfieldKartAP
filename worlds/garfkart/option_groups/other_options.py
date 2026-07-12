from __future__ import annotations

from dataclasses import dataclass
from Options import Choice, Range, Toggle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..world import GarfKartWorld


class RandomizeItems(Toggle):
    """
    Randomizes the items that can be received from item boxes and adds locations for
    acquiring each item from an item box for the first time.
    Always starts with one item unlocked.
    
    Incompatible with springs only.
    """
    display_name = "Randomize Items"

class LapSanity(Toggle):
    """
    Adds checks for finishing a lap in first place (or another place, configurable in mod settings), adding anywhere between 1 and 10
    items to the pool per race, for a total of 16 to 160 extra locations
    """
    display_name = "Lap Sanity"

class TrapPercentage(Range):
    """
    What percentage of filler items should be replaced with traps.
    """
    display_name = "Trap Percentage"
    
    range_start = 0
    range_end = 100
    default = 25
    
class TrapHandling(Choice):
    """
    Determines when traps are disabled. Some traps, such as Mirror Trap, override this option and will always disable after a period of time.
    
    - Time: Disables a trap sent after 1 minute of them being active in a race.
    - Race: Disables a trap sent after finishing a race, regardless of placement.
    - Win: Disables a trap sent after finishing a race in 1st place.
    """
    display_name = "Trap Handling"

    default = 0
    option_time = 0
    option_race = 1
    option_win = 2

class DeathLink(Toggle):
    """
    Enables Death Link.
    """
    display_name = "Death Link"