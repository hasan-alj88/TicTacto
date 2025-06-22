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

    def play(self, player: int, row: int, col: int):

        def row_col_check():
            if self.board[row, col] == "":
                pass_turn = True
            else:
                pass_turn = False
            return pass_turn

        def check_turn():
            if player % 2 == 1:
                x = 'X'
                return x
            elif player % 2 == 0:
                o = 'O'
                return o

        def token_place():
            if check_turn() == 'O':
                print("It's X's turn next")
                self.board[row, col] = 'O'
            elif check_turn() == 'X':
                print("It's O's turn next")
                self.board[row, col] = 'X'

        def check_winner():
            token = str
            if player % 2 == 1:
                token = 'O'
            if player % 2 == 0:
                token = 'X'
            for i in range(3):
                if np.all(self.board[i, :] == token):
                    self.winner = 0
                if np.all(self.board[:, i] == token):
                    self.winner = 0
                if np.all(np.diag(self.board) == token):
                    self.winner = 0
                if np.all(np.diag(np.fliplr(self.board)) == token):
                    self.winner = 0
            if self.winner == 0:
                print(f'{token} won')

        def move_remover():
            if check_turn() == 'X':
                if len(moves) > 4:
                    first_em = moves[0]
                    second_em = moves[1]
                    print(f'we are removing the oldest (X) move ({int(first_em) + 1}, {int(second_em + 1)})')
                    if len(moves) > 5:
                        self.board[moves[0], moves[1]] = ""
                        del moves[0:2]

            if check_turn() == 'O':
                if len(move) > 4:
                    first_elem = move[0]
                    second_elem = move[1]
                    print(f'we are removing the oldest (O) move ({int(first_elem) + 1}, {int(second_elem + 1)})')
                    if len(move) > 5:
                        self.board[move[0], move[1]] = ""
                        del move[0:2]

        def updater():
            move_remover()
            if row_col_check() is True:
                token_place()
                if check_turn() == 'X':
                    moves.append(row)
                    moves.append(col)
                if check_turn() == 'O':
                    move.append(row)
                    move.append(col)
                self.turn += 1
            else:
                print("that spot is taken, try again")

        check_winner()
        if game.winner == -1:
            while True:
                try:
                    row = int(input('row(1-3): ')) - 1
                    col = int(input('col(1-3): ')) - 1
                    valid = 3 >= row, 3 >= col
                    if not valid:
                        raise IndexError
                    if valid:
                        break
                except ValueError:
                    print("please enter values 1-3 only")
                except IndexError:
                    print("please enter values 1-3 only")
            updater()
            print(self.board)


if __name__ == '__main__':
    moves = []
    move = []
    game = TicTacTo()
    while game.winner == -1:
        game.play(player=game.turn, row=-1, col=-1)


