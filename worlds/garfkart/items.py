# This file should cover every item we could possibly need, even ones that are
# unimplemented as of writing this. There's a small chance we'll need to clean
# up unused ones on a full release
#
# The first ID (000, 100, 150) in every group is reserved for a progressive
# unlock item, even if one doesn't exist
#
# There's an argument to be made for fully writing out the item lists instead
# of generating a bunch of them with for loops for easy ID lookup, but 
# right now this is a whole lot easier on me.
 
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import GarfKartWorld

from BaseClasses import Item, ItemClassification
from .data import RACE_NAMES, CUP_NAMES, CHARACTER_NAMES, KART_NAMES, HAT_NAMES, SPOILER_NAMES
from .options import RandomizerType, is_cups_randomized, is_races_randomized

# Puzzle Pieces are named by race and numbered 1-3 to match the order 
# in which they are displayed in-game
PUZZLE_PIECE_TABLE = {
    "Puzzle Piece": 49
}
COURSE_ITEM_TABLE = {
    "Progressive Course Unlock": 100
}
CUP_ITEM_TABLE = {
    "Progressive Cup Unlock": 200,
    "Lasagna Cup": 201,
    "Pizza Cup": 202,
    "Burger Cup": 203,
    "Ice Cream Cup": 204,
}
CHARACTER_ITEM_TABLE = {}
KART_ITEM_TABLE = {}
HAT_ITEM_TABLE = {}
SPOILER_ITEM_TABLE = {}
ITEM_BOX_RANDOMIZER_TABLE = {
    "Item Unlock - Pie": 901,
    "Item Unlock - Homing Pie": 902,
    "Item Unlock - Diamond": 903,
    "Item Unlock - Magic Wand": 904,
    "Item Unlock - Perfume": 905,
    "Item Unlock - Lasagna": 906,
    "Item Unlock - UFO": 907,
    "Item Unlock - Pillow": 908,
    "Item Unlock - Spring": 909,
}

# Generate race-specific items:
# - Course Unlock
# - Puzzle piece 1-3
for index, race in enumerate(RACE_NAMES):
    course_unlock_name = f'{race} Course'

    # 3 puzzle pieces per race
    for n in range(3):
        name = f'{race} - Puzzle Piece {n + 1}'
        PUZZLE_PIECE_TABLE[name] = index * 3 + n + 1

    COURSE_ITEM_TABLE[course_unlock_name] = index + 101

# Generate 8 character unlock items
for index, character in enumerate(CHARACTER_NAMES):
    CHARACTER_ITEM_TABLE[character] = index + 301

# Generate 8 kart unlock items
for index, kart in enumerate(KART_NAMES):
    KART_ITEM_TABLE[kart] = index + 351

# Generate 24 hat unlock items
for index, hat in enumerate(HAT_NAMES):
    HAT_ITEM_TABLE[f'{hat}'] = index + 421

# Generate 12 spoiler unlock items
for index, spoiler in enumerate(SPOILER_NAMES):
    SPOILER_ITEM_TABLE[f'{spoiler}'] = index + 521

# Filler items reserve IDs 1000+
# Trap items reserve IDs 1500+
FILLER_ITEM_TABLE = {
    "Random Item Box": 1000, # Gives random item box next time player has an empty item slot
    "Start Boost Helper": 1001, # Guarantees perfect boost at start of next race
    "Stronger Item Boxes": 1002, # Adds item boxes that give 2 items for one race
    "Inspirational Garfield Quote": 1003, # Adds an inspirational (in garfields opinion) quote at the end of the race
}
TRAP_ITEM_TABLE = {
    "Mirror Trap": 1500, # Mirrors controls
    "Sleep Trap": 1501, # Puts you to sleep
    "Grayscale Trap": 1502, # Makes the race grayscale
    "Broken Drift Trap": 1503, # Makes blue drifts not possible
    "Bounce Trap": 1504, # Make you bounce in the air
}

# Combine them all into an item dict
ITEM_NAME_TO_ID = {
    **PUZZLE_PIECE_TABLE, # 48
    **COURSE_ITEM_TABLE, # 16
    **CUP_ITEM_TABLE, # 4
    **CHARACTER_ITEM_TABLE, # 8
    **KART_ITEM_TABLE, # 8
    **HAT_ITEM_TABLE, # 24
    **SPOILER_ITEM_TABLE, # 12
    **ITEM_BOX_RANDOMIZER_TABLE, # 8
    **FILLER_ITEM_TABLE, # as many as we want
    **TRAP_ITEM_TABLE # as many as we want
}

# Progression items
PROGRESSION_ITEMS = [
    *COURSE_ITEM_TABLE,
    *CUP_ITEM_TABLE
]

class GarfKartItem(Item):
    game = "Garfield Kart - Furious Racing"


############# 
# Functions #
#############
def get_n_named_puzzle_pieces(n) -> list[str]:
    puzzle_pieces = []

    if n == 0:
        return []

    for race in RACE_NAMES:
        for i in range(3):
            puzzle_pieces.append(f'{race} - Puzzle Piece {i+1}')
            if len(puzzle_pieces) == n:
                return puzzle_pieces
            
    return puzzle_pieces

@dataclass
class ItemState:
    starting_item: GarfKartItem
    pool_items: list[GarfKartItem]

def create_randomized_item_state(world: GarfKartWorld, items):
    shuffled_items = list(items) # Make a copy to avoid mutation
    world.random.shuffle(shuffled_items)
    starting_item = shuffled_items.pop()
    starting_object = world.create_item(starting_item)
    item_objects = [
        world.create_item(item) for item in shuffled_items
    ]

    return ItemState(starting_object, item_objects)

def get_random_filler_item(world: GarfKartWorld) -> str:
    # TODO: Include traps

    items = list(FILLER_ITEM_TABLE)

    if world.options.randomize_puzzle_pieces and world.options.goal != "puzzle_piece_hunt":
        items += ["Puzzle Piece"]

    return world.random.choice(items)

def create_item_object(world: GarfKartWorld, name: str):
    classification = ItemClassification.useful

    # Progression items are progression items
    if name in PROGRESSION_ITEMS:
        classification = ItemClassification.progression

    # Deprioritize puzzle pieces
    if name == "Puzzle Piece":
        if world.options.goal == "puzzle_piece_hunt":
            classification = ItemClassification.progression_deprioritized_skip_balancing
        else:
            classification = ItemClassification.filler

    # Item unlocks are priority items to reach the item acquisition checks
    if world.options.randomize_items:
        if "Item Unlock" in name:
            classification = ItemClassification.progression_deprioritized_skip_balancing

        # Spring and Lasagna item unlocks are progression sometimes
        if world.options.randomize_puzzle_pieces:
            if name in ["Item Unlock - Spring", "Item Unlock - Lasagna"]:
                classification = ItemClassification.progression

    if name in KART_NAMES or name in CHARACTER_NAMES:
        classification = ItemClassification.progression_deprioritized_skip_balancing

    # Filler is filler (no way!)
    if name in FILLER_ITEM_TABLE:
        classification = ItemClassification.filler

    # Traps are traps
    if name in TRAP_ITEM_TABLE:
        classification = ItemClassification.trap

    return GarfKartItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_itempool(world: GarfKartWorld) -> None:
    itempool: list[Item] = []

    randomize_races = is_races_randomized(world) == RandomizerType.random
    randomize_cups = is_cups_randomized(world) == RandomizerType.random

    # Add race victory locations
    if randomize_races:
        state = create_randomized_item_state(world, [
            f'{race} Course' for race in RACE_NAMES
        ])

        world.push_precollected(state.starting_item)
        itempool += state.pool_items

    # Add cup victory locations
    if randomize_cups:
        if world.options.progressive_cups:
            itempool += [
                world.create_item("Progressive Cup Unlock"),
                world.create_item("Progressive Cup Unlock"),
                world.create_item("Progressive Cup Unlock"),
            ]

        else:

            # Don't start with a random cup if randomize_races is also on, only
            # give a random starting cup if there's otherwise no progression
            # possible at all
            item_names = [
                cup for cup in CUP_NAMES
            ]
            if randomize_races:
                itempool += [
                    world.create_item(item) for item in item_names
                ]
            else:
                state = create_randomized_item_state(world, item_names)
                world.push_precollected(state.starting_item)
                itempool += state.pool_items

    # randomize_puzzle_pieces is automatically set to True if the goal is 
    # Puzzle Piece Hunt, so we don't need to check both.
    if world.options.randomize_puzzle_pieces:
        itempool += [
            world.create_item("Puzzle Piece") for _ in range(world.options.puzzle_piece_count)
        ]

    # Character and Kart randomizer
    if world.options.randomize_characters:
        state = create_randomized_item_state(world, [
            character for character in CHARACTER_NAMES
        ])
        world.push_precollected(state.starting_item)
        itempool += state.pool_items

    if world.options.randomize_karts:
        state = create_randomized_item_state(world, [
            kart for kart in KART_NAMES
        ])
        world.push_precollected(state.starting_item)
        itempool += state.pool_items

    if world.options.randomize_hats:
        itempool += [
            world.create_item(hat) for hat in HAT_NAMES
        ]

    if world.options.randomize_spoilers:
        itempool += [
            world.create_item(spoiler) for spoiler in SPOILER_NAMES
        ]

    # Item randomizer!
    if world.options.randomize_items:
        if world.options.springs_only:
            itempool += [
                world.create_item('Item Unlock - Spring')
            ]
        else:
            state = create_randomized_item_state(world, ITEM_BOX_RANDOMIZER_TABLE)
            world.push_precollected(state.starting_item)
            itempool += state.pool_items

    # Compare item pool size to location size, and fill what's left with
    # filler items.
    item_count = len(itempool)
    unfilled_location_count = len(world.multiworld.get_unfilled_locations(world.player))
    filler_item_count = unfilled_location_count - item_count
    
    itempool += [
        world.create_filler() for _ in range(filler_item_count)
    ]

    # Append the item pool to the world's
    world.multiworld.itempool += itempool
