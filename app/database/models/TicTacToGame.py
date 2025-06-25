from datetime import datetime

import numpy as np
from sqlmodel import SQLModel

from Utils.DataTypeConversions import numpy2json


class TicTacToeGames(SQLModel, table=True):
    __tablename__ = "tic_tac_toe_games"
    id: int = SQLModel.Field(primary_key=True, default=None, index=True)
    player_one_id: int = SQLModel.Field(foreign_key="users.id")
    player_two_id: int = SQLModel.Field(foreign_key="users.id")
    turn: int = SQLModel.Field(default=0)


class TicTacToeMoveHistory(SQLModel, table=True):
    __tablename__ = "tic_tac_toe_move_history"
    id: int = SQLModel.Field(primary_key=True, default=None, index=True)
    game_id: int = SQLModel.Field(foreign_key="tic_tac_toe_games.id")
    player_id: int = SQLModel.Field(foreign_key="users.id")
    row: int
    col: int
    created_at: datetime = SQLModel.Field(default=datetime.utcnow())