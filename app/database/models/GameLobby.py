from datetime import datetime
from enum import IntEnum
from typing import Optional
from sqlmodel import (SQLModel, Field, Column, DateTime,Computed, Boolean, func)


class Games(SQLModel, table=True):
    __tablename__ = "games"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    created_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now')
        )
    )
    available: bool = True
    icon: str

class GameLobbyOnlineUsers(SQLModel, table=True):
    __tablename__ = "game_lobby_online_users"
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="games.id")
    user_id: int = Field(foreign_key="users.id")
    online_from: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now')
        )
    )
    online_to: Optional[datetime] = None
    is_online: bool = Field(
        sa_column=Column(
            Boolean,
            Computed("online_to IS NULL OR datetime('now') < online_to")
        )
    )

class GameInvitationStatus(IntEnum):
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    EXPIRED = 4

class GameInvites(SQLModel, table=True):
    __tablename__ = "game_invites"
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="games.id")
    inviter_id: int = Field(foreign_key="users.id")
    invitee_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now')
        )
    )
    accepted: GameInvitationStatus = Field(default=GameInvitationStatus.PENDING)


class GamesInSession(SQLModel, table=True):
    __tablename__ = "games_in_session"
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="games.id")
    started_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now')
        )
    )
    ended_at: Optional[datetime] = None

class GameWinStatus(IntEnum):
    PENDING = 1
    DRAW = 2
    WINNER = 3
    WITHDRAW = 4

class GameSessionPlayers(SQLModel, table=True):
    __tablename__ = "game_session_players"
    id: Optional[int] = Field(default=None, primary_key=True)
    game_session_id: int = Field(foreign_key="games_in_session.id")
    user_id: int = Field(foreign_key="users.id")
    joined_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now')
        )
    )
    win_status: GameWinStatus = Field(default=GameWinStatus.PENDING)