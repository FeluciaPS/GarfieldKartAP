

from collections.abc import Mapping
from typing import Any
from Options import OptionError
from worlds.AutoWorld import World
from .data import CHARACTER_NAMES, KART_NAMES, get_random_stat

from . import items, locations, options, regions, rules, web_world

# I'll be calling these classes GarfKart because GarfieldKartFuriousRacing
# is way too long and I don't believe for a second anyone's going to
# randomize the original Garfield Kart, so there shouldn't be an issue
# using that class name.
class GarfKartWorld(World):
    """
    Garfield Kart - Furious Racing is a chaotic kart racer featuring
    everyone's favourite orange cat and plenty of lasagna.
    """

    game = "Garfield Kart - Furious Racing"

    web = web_world.GarfKartWebWorld()

    options_dataclass = options.GarfKartOptions
    options: options.GarfKartOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    # Make UT generate without yaml
    ut_can_gen_without_yaml = True

    # Stat randomizer stuff
    randomized_stats = {}

    def generate_random_stats(self):
        self.randomized_stats = {}

        mean = 0
        match self.options.random_stat_values:
            case "low":
                mean = -20
            case "medium":
                mean = 0
            case "high":
                mean = 15

        if self.options.stat_randomizer in ["karts", "both"]:
            random_kart_stats = {}
            for name in KART_NAMES:
                # Okay listen, it's called Maniability in the game code so we're
                # using maniability here. It's handling, it's just handling, but
                # this makes the mod easier to deal with.
                random_kart_stats[name] = {
                    "Acceleration": get_random_stat(self, mean),
                    "Speed": get_random_stat(self, mean),
                    "Maniability": get_random_stat(self, mean)
                }
            self.randomized_stats["karts"] = random_kart_stats
                
        if self.options.stat_randomizer in ["characters", "both"]:
            random_character_stats = {}
            for name in CHARACTER_NAMES:
                # Again, maniability = handling
                random_character_stats[name] = {
                    "Acceleration": get_random_stat(self, mean),
                    "Speed": get_random_stat(self, mean),
                    "Maniability": get_random_stat(self, mean)
                }
            self.randomized_stats["characters"] = random_character_stats

    # TODO: this shouldn't end up in v1.0
    def pre_fill(self):
        from BaseClasses import CollectionState
        from Fill import sweep_from_pool
        state = sweep_from_pool(CollectionState(self.multiworld), self.multiworld.itempool)
        unreachable_locations = [location for location in self.get_locations() if not location.can_reach(state)]

        # I'm not good with exception types I'm sure "Exception" covers it
        if len(unreachable_locations):
            raise Exception(f"There are unreachable locations, please let Felucia know: {unreachable_locations}")
        if not len(self.multiworld.itempool):
            raise OptionError("There aren't any items in the item pool. Let Felucia know this is a bug.")

    def generate_early(self):
        # Handle Universal Tracker support
        ut_slot_options: dict[str, Any] | None = None
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            ut_slot_options = slot_data.get("options", {})
            for key, value in ut_slot_options.items():
                if key == "lap_count":
                    continue
                opt = getattr(self.options, key, None)
                if opt is not None:
                    setattr(self.options, key, opt.from_any(value))

        if self.options.goal == "puzzle_piece_hunt":
            self.options.randomize_puzzle_pieces.value = True

        # The Time Trials goal requires time trial checks - force at least bronze to avoid OptionError
        if self.options.goal == "time_trials" and not self.options.time_trial_randomization:
            self.options.time_trial_randomization.value = options.TimeTrialRandomization.option_bronze

        if self.options.item_mania:
            self.options.disable_cpu_items.value = False

        # Springs Only and Randomize Items are incompatible
        if self.options.springs_only:
            self.options.randomize_items.value = False

        # Progressive Cups and Cups & Races are incompatible - too much fill pressure
        if self.options.progressive_cups and self.options.randomize_races == "cups_and_races":
            self.options.progressive_cups.value = False

        self.lap_count = self.options.lap_count.value
        if self.options.single_lap_mode:
            self.lap_count = 1

        # Universal Tracker: use the exact lap count from the original gen
        if ut_slot_options is not None and "lap_count" in ut_slot_options:
            self.lap_count = ut_slot_options["lap_count"]

        # Stat randomizer
        self.generate_random_stats()

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_itempool(self)

    def create_item(self, name: str) -> items.GarfKartItem:
        return items.create_item_object(self, name)

    def write_spoiler(self, spoiler_handle):
        if self.options.stat_randomizer in ["characters", "karts", "both"]:
            spoiler_handle.write(f'\n\n{self.player_name}: Stat randomizer values (Accel, Speed, Handling)\n\n')

            if self.options.stat_randomizer in ["characters", "both"]:
                for name in CHARACTER_NAMES:
                    stats = self.randomized_stats["characters"][name]
                    spoiler_handle.write(f'{name}: {stats["Acceleration"]}, {stats["Speed"]}, {stats["Maniability"]}\n')

            if self.options.stat_randomizer in ["karts", "both"]:
                for name in KART_NAMES:
                    stats = self.randomized_stats["karts"][name]
                    spoiler_handle.write(f'{name}: {stats["Acceleration"]}, {stats["Speed"]}, {stats["Maniability"]}\n')

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item(self)
    
    # Copied from APQuest for the time being
    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = dict()

        slot_data["randomized_stats"] = self.randomized_stats

        slot_data["options"] = self.options.as_dict(
            # Goal Options
            "goal",
            "cc_requirement",
            "time_trial_goal_grade",
            "time_trial_randomization",

            # Race Randomizer Options
            "randomize_races",
            "progressive_cups",

            # Puzzle Piece Options
            "randomize_puzzle_pieces",
            "puzzle_piece_count",
            "puzzle_piece_required",

            # Character Options
            "randomize_characters",
            "randomize_karts",
            "randomize_hats",
            "randomize_spoilers",
            "stat_randomizer",
            "random_stat_values",

            # Game Options
            "single_lap_mode",
            "lap_count",
            "disable_cpu_items",
            "item_mania",
            "springs_only",

            # Other Randomizer Options
            "randomize_items",
            "lap_sanity",
            "trap_percentage",
            "trap_handling",
            "death_link"
        )

        slot_data["options"]["lap_count"] = self.lap_count

        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Returning a truthy value here tells Universal Tracker to re-generate
        # the world with the slot data
        return slot_data
