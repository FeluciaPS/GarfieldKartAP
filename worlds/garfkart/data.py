"""Contains data objects used to generate items, locations, and rules"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import GarfKartWorld

# List of race names in order of appearance
RACE_NAMES = [
    "Catz in the Hood",
    "Crazy Dunes",
    "Palerock Lake",
    "City Slicker",
    "Country Bumpkin",
    "Spooky Manor",
    "Mally Market",
    "Valley of the Kings",
    "Misty for Me",
    "Sneak-a-Peak",
    "Blazing Oasis",
    "Pastacosi Factory",
    "Mysterious Temple",
    "Prohibited Site",
    "Caskou Park",
    "Loopy Lagoon"
]

# Dict of races in each cup
RACES_BY_CUP = {
    "Lasagna Cup": [
        "Catz in the Hood",
        "Crazy Dunes",
        "Palerock Lake",
        "City Slicker"
    ],
    "Pizza Cup": [
        "Country Bumpkin",
        "Spooky Manor",
        "Mally Market",
        "Valley of the Kings"
    ],
    "Burger Cup": [
        "Misty for Me",
        "Sneak-a-Peak",
        "Blazing Oasis",
        "Pastacosi Factory"
    ],
    "Ice Cream Cup": [
        "Mysterious Temple",
        "Prohibited Site",
        "Caskou Park",
        "Loopy Lagoon"
    ]
}

CUPS_BY_RACE = {}
for cup in RACES_BY_CUP:
    for race in RACES_BY_CUP[cup]:
        CUPS_BY_RACE[race] = cup

# List of cup names in order of appearance
# The order of these matters for Progressive Cup Unlock logic
CUP_NAMES = [
    "Lasagna Cup",
    "Pizza Cup",
    "Burger Cup",
    "Ice Cream Cup",
]

CHARACTER_NAMES = [
    "Garfield",
    "Jon",
    "Liz",
    "Odie", 
    "Arlene",
    "Nermal",
    "Squeak",
    "Harry",
]

KART_NAMES = [
    "Formula Zzzz",
    "Abstract-Kart",
    "Medi-Kart",
    "Woof-Mobile",
    "Kissy-Kart",
    "Cutie-Pie Cat",
    "Rat-Racer",
    "Muck-Madness",
]

HAT_NAMES = [
    "Beddy-Bye Cap",
    "Whizzy Wizard",
    "Tic-Toque",
    "Elasto-Hat",
    "Chef's Special",
    "Cutie-Pie Crown",
    "Viking Helmet",
    "Stink-O-Rama",

    # Unique character hats
    "Space Bubble", # Garfield
    "Pizzaiolo Hat", # Jon
    "Bunny Band", # Liz
    "Joe Montagna", # Odie
    "Aristo-Catic Bicorn", # Arlene
    "Toutankhameow", # Nermal
    "Apprentice Sorcerer", # Squeak
    "Mule Head", # Harry
]

SPOILER_NAMES = [
    "Bombastic Spoiler",
    "Whacky Spoiler",
    "Superfit Spoiler",
    "Cyclobone Spoiler",
    "Foxy Spoiler",
    "Shimmering Spoiler",
    "Holey Moley Spoiler",
    "Stained Spoiler",
]

ITEM_NAMES = [
    "Pie",
    "Homing Pie",
    "Diamond",
    "Magic Wand",
    "Perfume",
    "Lasagna",
    "UFO",
    "Pillow",
    "Spring",
]

# Some puzzle pieces logically require items which is relevant for the
# item randomizer
class PuzzlePieceRequirements:
    Nothing = 0 # Probably unused 
    Spring = 1 # Spring
    Lasagna = 2 # Lasagna
    Either = 3 # Lasagna or Spring

# Dictionary of puzzle pieces and their required items
PUZZLE_PIECE_REQUIREMENTS = {
    "Catz in the Hood": {
        2: PuzzlePieceRequirements.Spring,
    },
    "Crazy Dunes": {
        1: PuzzlePieceRequirements.Spring,
        2: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Either,
    },
    "Palerock Lake": {
        2: PuzzlePieceRequirements.Spring,
    },
    "City Slicker": {
        1: PuzzlePieceRequirements.Spring,
        2: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Spring,
    },
    "Country Bumpkin": {},
    "Spooky Manor": {
        1: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Spring,
    },
    "Mally Market": {
        1: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Spring,
    },
    "Valley of the Kings": {
        2: PuzzlePieceRequirements.Spring,
    },
    "Misty for Me": {
        1: PuzzlePieceRequirements.Spring,
        2: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Spring,
    },
    "Sneak-a-Peak": {
        1: PuzzlePieceRequirements.Spring,
        2: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Lasagna, # Can also be done with spring, but this should be considered out of logic cause its way easier with Lasagna
    },
    "Blazing Oasis": {
        1: PuzzlePieceRequirements.Spring,
        2: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Either,
    },
    "Pastacosi Factory": {
        1: PuzzlePieceRequirements.Spring,
    },
    "Mysterious Temple": {
        1: PuzzlePieceRequirements.Spring,
        2: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Spring,
    },
    "Prohibited Site": {
        2: PuzzlePieceRequirements.Spring,
        3: PuzzlePieceRequirements.Spring,
    },
    "Caskou Park": {
        3: PuzzlePieceRequirements.Spring,
    },
    "Loopy Lagoon": {
        3: PuzzlePieceRequirements.Spring,
    },
}

def get_random_stat(world: GarfKartWorld, mean, min_value=-30, max_value=25, std_dev=10):
    if not (min_value <= mean <= max_value):
        raise ValueError("Normal distribution mean must be within the min/max boundaries.")

    # Reroll up to 5 times if the value is outside the boundaries
    for _ in range(5):
        value = world.random.gauss(mean, std_dev)
        value = round(value, 2)
        if min_value <= value <= max_value:
            return value

    # In the unlikely event that it's still outside the boundaries, just 
    # clamp it 
    return max(min_value, min(value, max_value))