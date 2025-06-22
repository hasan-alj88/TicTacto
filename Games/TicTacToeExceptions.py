

class NotYourTurn(ValueError):
    def __init__(self, player: int, player_turn: int):
        super().__init__(f"It's not player {player}'s turn. It's player {player_turn}'s turn.")


class InvalidPlayer(ValueError):
    def __init__(self, player: int):
        super().__init__(f"Player {player} is not a valid player.")


class InvalidMove(ValueError):
    def __init__(self, move: str):
        super().__init__(f"Move {move} is not a valid move.")