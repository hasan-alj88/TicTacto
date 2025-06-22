from dataclasses import dataclass, field
from typing import Dict, Tuple, List
from typing import ClassVar

import logfire
import numpy as np
from decouple import config

from Games.TicTacToeExceptions import NotYourTurn, InvalidPlayer, InvalidMove

logfire.configure(
    token=config('LOGFIRE_TOKEN'),
    service_name=config('LOGFIRE_SERVICE_NAME'),
    environment=config('LOGFIRE_ENVIRONMENT', default='dev'),
    data_dir='logs'
)

@dataclass
class TicTacTo:
    board: np.ndarray[str] = field(
        default_factory=lambda: np.full((3, 3), ""), init=False
    )
    winner: int = field(default=-1, init=False)
    turn: int = field(default=0, init=False)
    players: Dict[int, str] = field(default_factory=lambda: {0:'X', 1:'O'}, init=False)
    history: Dict[str, List[Tuple[int, int]]] = field(default_factory=lambda: {'X':[], 'O':[]}, init=False)

    @property
    def is_in_progress(self)-> bool:
        return self.winner == -1

    def is_occupied(self, row, col)-> bool:
        try:
            return self.board[row, col] == ""
        except IndexError:
            raise InvalidMove(f"[{row}, {col}] is out of bounds")

    def check_winner(self, player: int):
        token = self.players[player]

        for i in range(3):
            if np.all(self.board[i, :] == token):
                self.winner = player
            if np.all(self.board[:, i] == token):
                self.winner = player
            if np.all(np.diag(self.board) == token):
                self.winner = player
            if np.all(np.diag(np.fliplr(self.board)) == token):
                self.winner = player
        if self.winner == player:
            logfire.info(f"player {player}[{token}] won the game")

    def player_validation(self,player: int):
        if player != self.turn:
            raise NotYourTurn(player, self.turn)

    def place_token(self,player:int, row: int, col: int):
        self.player_validation(player)
        try:
            token = self.players[player]
        except KeyError:
            raise InvalidPlayer(player)

        if not self.is_occupied(row, col):
            raise InvalidMove(f"[{row}, {col}] is occupied")

        self.board[row, col] = token
        logfire.info(f"player {player} placed {token} at [{row}, {col}]")

        self.history[token].append((row, col))
        if len(self.history[token]) == 4:
            oldest_move = self.history[token][0]
            self.board[*oldest_move] = ""
            logfire.info(f"Oldest move of player {player}[{token}] on ({row}, {col}) was removed)")
            del self.history[token][0]

    def display_board(self):
        print(self.board)

    def board_html(self, include_css: bool = True):
        """
        Convert a 3x3 numpy array representing a tic-tac-toe board to HTML component.

        Args:
            board (numpy.ndarray): 3x3 array with 'X', 'O', or '' (empty string)
            include_css (bool): Whether to include CSS styles (default: True)

        Returns:
            str: HTML component string representing the tic-tac-toe board
        """
        css = ""
        if include_css:
            css = """
        <style>
        .tictactoe-board {
            display: grid;
            grid-template-columns: repeat(3, 80px);
            grid-template-rows: repeat(3, 80px);
            gap: 2px;
            background-color: #333;
            padding: 2px;
            border-radius: 8px;
            margin: 0 auto;
        }
        .tictactoe-cell {
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 28px;
            font-weight: bold;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        .tictactoe-cell.x {
            color: #ff4757;
        }
        .tictactoe-cell.o {
            color: #3742fa;
        }
        .tictactoe-cell:empty {
            background-color: #fafafa;
        }
        </style>
        """

        html = css + '<div class="tictactoe-board">\n'

        # Generate cells for the 3x3 grid
        for i in range(3):
            for j in range(3):
                cell_value = self.board[i, j]
                cell_class = ""
                cell_content = ""

                if cell_value == 'X':
                    cell_class = " x"
                    cell_content = "X"
                elif cell_value == 'O':
                    cell_class = " o"
                    cell_content = "O"
                # Empty cells ('') will have no content and no special class

                html += f'    <div class="tictactoe-cell{cell_class}">{cell_content}</div>\n'

        html += '</div>'

        return html

    def play(self, player: int, row: int, col: int):
        row, col = int(row)-1, int(col)-1
        logfire.info(f"player {player} is playing. Checking his turn")
        self.place_token(player, row, col)
        self.turn = (player + 1) % 2
        logfire.info(f"player {player} is now up for next turn")
        self.check_winner(player)



if __name__ == '__main__':
    moves = []
    move = []
    game = TicTacTo()
    while game.is_in_progress:
        row, col = input("Enter row and column: ").split()
        game.play(player=game.turn, row=int(row), col=int(col))
        game.display_board()


