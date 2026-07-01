from __future__ import annotations

from dataclasses import dataclass
from Options import Choice, Toggle, DefaultOnToggle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..world import GarfKartWorld
    

class RandomizeCharacters(DefaultOnToggle):
    """
    Adds characters to the item pool, and adds a location for winning a race as each character.
    """
    display_name = "Randomize Characters"

class RandomizeKarts(DefaultOnToggle):
    """
    Adds karts to the item pool, and adds a location for winning a race with each kart.
    """
    display_name = "Randomize Karts"

class RandomizeHats(DefaultOnToggle):
    """
    Adds hats to the item pool, and adds locatiosn for unlocking a hat via winning a single race or time trial
    """
    display_name = "Randomize Hats"

class RandomizeSpoilers(Toggle):
    """
    Adds spoilers to the item pool, and adds locations for unlocking spoilers via grand prix 1st place finishes
    """
    display_name = "Randomize Spoilers"

class StatRandomizer(Choice):
    """
    Randomizes the top speed, acceleration, and handling for Karts and/or Characters

    - Off: Karts and characters use their default values
    - Karts: Randomizes kart stats, not characters
    - Characters: Randomizes character stats, not karts
    - Both: Randomizes stats for both karts and characters.
    """
    display_name = "Stat Randomizer"
    default = 0

    option_off = 0
    option_karts  = 1
    option_characters = 2
    option_both = 3

class RandomStatValues(Choice):
    """
    Choose how high you want randomized stats to be. Note that these are just
    averages and outliers may still happen, they're just less likely.

    - Low: Stats are generally much lower than the base game
    - Medium: Stats are generally around the same as the base game
    - High: Stats are generally much higher than the base game

    !! WARNING: Setting this to low is extremely likely make certain vanilla 
    time trial medals impossible !!
    """
    display_name = "Random Stat Values"
    default = 1

    option_low = 0
    option_medium = 1
    option_high = 2