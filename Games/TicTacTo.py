from dataclasses import dataclass, field
from typing import Dict

import numpy as np


@dataclass
class TicTacTo:
    board: np.ndarray[str] = field(
        default_factory=lambda: np.full((3, 3), ""), init=False
    )
    winner: int = field(default=-1, init=False)
    turn: int = field(default=1, init=False)
    players: Dict[int, str] = field(default_factory=lambda: {1:'X', 2:'O'}, init=False)

    def play(self,player: int, row: int, col: int) -> None:
        # confirm that it is his turn

        # confirm that the (row, col) not occupied

        # place player's token in board at (row,col)

        # update run

        # check if someone wins

    def check_winner(self) -> bool:
        pass


