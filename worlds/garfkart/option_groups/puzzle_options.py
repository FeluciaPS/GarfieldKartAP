from __future__ import annotations

from dataclasses import dataclass
from Options import Range, Toggle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..world import GarfKartWorld


class RandomizePuzzlePieces(Toggle):
    """
    Adds puzzle pieces to the item pool.
    
    Always on when the goal is Puzzle Piece Hunt
    """
    display_name = "Randomize Puzzle Pieces"

class PuzzlePieceCount(Range):
    """
    Sets the amount of puzzle pieces added to the item pool. If the goal is Puzzle Piece Hunt,
    a percentage of these (set by Puzzle Pieces Required) is required to beat the game.

    If puzzle pieces aren't randomized, this option does nothing.
    """

    display_name = "Puzzle Piece Count"

    range_start = 1
    range_end = 48
    default = 48
    
class PuzzlePieceRequired(Range):
    """
    Sets the percentage of the puzzle pieces in the item pool required to beat the game.

    Does nothing if the goal is not Puzzle Piece Hunt.
    """

    display_name = "Puzzle Pieces Required"

    range_start = 10
    range_end = 100
    default = 75
