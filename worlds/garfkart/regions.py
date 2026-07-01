# Region structure starts with the origin (Main Menu) region
# Then probably splits regions by course/cup
#
# The reason for not structuring it like Main Menu->Cup->Course is 
# that makes individual courses logically inaccessible if you can't 
# access the corresponding cup, which might be undesirable in the future.
#
# I don't see a purpose in setting up some deep logical structure for regions
# as of now. Most logic will end up pretty simple and can be done at the 
# location level instead.

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import GarfKartWorld

from BaseClasses import Region
from worlds.garfkart.data import CUP_NAMES, RACE_NAMES


def create_and_connect_regions(world: GarfKartWorld):
    create_regions(world)
    connect_regions(world)

def create_regions(world: GarfKartWorld):

    # Menu is its own region, it serves as the origin region.
    menu = Region("Menu", world.player, world.multiworld)
    
    regions = [
        menu
    ]

    # Each race gets its own region, containing puzzle pieces, race victories
    # and time trials
    regions += [
        Region(race, world.player, world.multiworld) for race in RACE_NAMES
    ]

    # Each cup gets its own region containing cup victories and spoiler unlocks
    regions += [
        Region(cup, world.player, world.multiworld) for cup in CUP_NAMES
    ]

    # Time trials get their own regions so they can be reached via either the
    # course unlock or the owning cup, independent of the stricter race regions
    if world.options.time_trial_randomization:
        regions += [
            Region(f"{race} Time Trials", world.player, world.multiworld) for race in RACE_NAMES
        ]

    world.multiworld.regions += regions

def connect_regions(world: GarfKartWorld):
    menu = world.get_region("Menu")

    for race in RACE_NAMES:
        region = world.get_region(race)
        menu.connect(region, race)

    for cup in CUP_NAMES:
        region = world.get_region(cup)
        menu.connect(region, cup)

    if world.options.time_trial_randomization:
        for race in RACE_NAMES:
            region = world.get_region(f"{race} Time Trials")
            menu.connect(region, f"{race} Time Trials")