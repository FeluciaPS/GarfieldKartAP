from __future__ import annotations

# Logic goes here

import math

from .data import KART_NAMES, CHARACTER_NAMES, CUP_NAMES, CUPS_BY_RACE, ITEM_NAMES, PUZZLE_PIECE_REQUIREMENTS, RACE_NAMES, RACES_BY_CUP, PuzzlePieceRequirements
from .options import RandomizerType, is_cups_randomized, is_races_randomized

from rule_builder.rules import Has, HasAllCounts, HasAny

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import GarfKartWorld


def set_all_rules(world: GarfKartWorld):
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def get_required_cup_items(cup: str, randomize_races: bool, randomize_cups: bool, progressive_cups: bool) -> dict[str, int]:
    items = {}
    if randomize_cups:
        if progressive_cups:
            index = CUP_NAMES.index(cup)
            if index > 0:
                items["Progressive Cup Unlock"] = index
        else:
            items[cup] = 1

    if randomize_races:
        for race in RACES_BY_CUP[cup]:
            items[f"{race} Course"] = 1

    return items

def get_required_race_items(race, randomize_races: bool, randomize_cups: bool, progressive_cups: bool) -> dict[str, int]:
    items = {}
    if randomize_races:
        items[f"{race} Course"] = 1

    elif randomize_cups:
        # Only if randomize_races is False should we lock races until the cup is
        # unlocked
        if progressive_cups:
            index = CUP_NAMES.index(CUPS_BY_RACE[race])
            if index > 0:
                items["Progressive Cup Unlock"] = index
        else:
            items[CUPS_BY_RACE[race]] = 1

    return items

def get_time_trial_access_rule(race, randomize_races: bool, randomize_cups: bool, progressive_cups: bool):
    """
    A course's time trials are in logic once the course can be reached by ANY
    unlock - its own course unlock OR the cup it belongs to. Returns a rule, or
    None when the course is always reachable (nothing gating it).
    """
    clauses = []

    if randomize_races:
        clauses.append(Has(f"{race} Course"))

    if randomize_cups:
        cup = CUPS_BY_RACE[race]
        if progressive_cups:
            index = CUP_NAMES.index(cup)
            if index == 0:
                # The first cup is always unlocked, so this path is always open
                return None
            clauses.append(Has("Progressive Cup Unlock", index))
        else:
            clauses.append(Has(cup))

    if not clauses:
        return None

    rule = clauses[0]
    for clause in clauses[1:]:
        rule |= clause
    return rule

def set_all_entrance_rules(world: GarfKartWorld):
    # Store these in a variable to reduce redundancy
    randomize_races = is_races_randomized(world) == RandomizerType.random
    randomize_cups = is_cups_randomized(world) == RandomizerType.random

    # Set cup unlock rules
    for cup in CUP_NAMES:
        cup_entrance = world.get_entrance(cup)
        required_items = get_required_cup_items(
            cup,
            randomize_races,
            randomize_cups,
            world.options.progressive_cups
        )

        if len(required_items) == 0:
            continue

        world.set_rule(cup_entrance, HasAllCounts(required_items))

    # Set race unlock rules
    for race in RACE_NAMES:
        race_entrance = world.get_entrance(race)
        required_items = get_required_race_items(
            race,
            randomize_races,
            randomize_cups,
            world.options.progressive_cups
        )

        if len(required_items) == 0:
            continue

        world.set_rule(race_entrance, HasAllCounts(required_items))

    if world.options.time_trial_randomization:
        for race in RACE_NAMES:
            rule = get_time_trial_access_rule(
                race, randomize_races, randomize_cups, world.options.progressive_cups
            )
            if rule is None:
                continue

            world.set_rule(world.get_entrance(f"{race} Time Trials"), rule)

def set_all_location_rules(world: GarfKartWorld):

    # Winning a race as a character also requires having the character unlock
    if world.options.randomize_characters:
        for character in CHARACTER_NAMES:
            location = world.get_location(f'Win Race as {character}')
            world.set_rule(location, Has(character))

    # And same for karts
    if world.options.randomize_karts:
        for kart in KART_NAMES:
            location = world.get_location(f'Win Race with {kart}')
            world.set_rule(location, Has(kart))

    # Certain puzzle pieces require a Spring or Lasagna item to be accessed
    if world.options.randomize_puzzle_pieces and world.options.randomize_items:
        for race in PUZZLE_PIECE_REQUIREMENTS:
            for piece in PUZZLE_PIECE_REQUIREMENTS[race]:
                location = world.get_location(f'{race}: Puzzle Piece {piece}')
                required_items = [
                    "Item Unlock - Spring"
                ]

                if PUZZLE_PIECE_REQUIREMENTS[race][piece] == PuzzlePieceRequirements.Either and not world.options.springs_only:
                    required_items.append("Item Unlock - Lasagna")

                world.set_rule(location, HasAny(*required_items))

    # Item acquisition locations can't be accessed until you have the associated item
    if world.options.randomize_items:
        if world.options.springs_only:
            location = world.get_location("Find Item: Spring")
            world.set_rule(location, Has("Item Unlock - Spring"))
        else:
            for item in ITEM_NAMES:
                location = world.get_location(f'Find Item: {item}')
                world.set_rule(location, Has(f"Item Unlock - {item}"))

def get_required_puzzle_pieces(world: GarfKartWorld) -> int:
    return math.ceil(world.options.puzzle_piece_count.value * world.options.puzzle_piece_required.value / 100)

def set_completion_condition(world: GarfKartWorld):
    randomize_races = is_races_randomized(world) == RandomizerType.random
    randomize_cups = is_cups_randomized(world) == RandomizerType.random

    # Build on a single required_items dict, adding required items depending
    # on various victory conditions, this is nice because a lot of them have
    # partial overlap
    required_items = {}

    if world.options.goal == "grand_prix":
        # The game can be completed if all cups can be reached
        for cup in CUP_NAMES:
            required_items = {
                **required_items,
                **get_required_cup_items(cup, randomize_races, randomize_cups, world.options.progressive_cups)
            }

    # Both the Races and Time Trials goals are beaten once every race is
    # accessible - time trials are assumed always beatable once you can reach
    # their course.
    if world.options.goal in ["races", "time_trials"]:
        for race in RACE_NAMES:
            required_items = {
                **required_items,
                **get_required_race_items(race, randomize_races, randomize_cups, world.options.progressive_cups)
            }

    if world.options.goal == "puzzle_piece_hunt":
        required_items["Puzzle Piece"] = get_required_puzzle_pieces(world)

    # HasAllCounts resolves an empty mapping to True_, matching the old
    # state.has_all_counts({}) behaviour for goals without unlock requirements
    world.set_completion_rule(HasAllCounts(required_items))
