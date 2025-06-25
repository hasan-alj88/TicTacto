from typing import List

import logfire
from fastapi import APIRouter, Request, Depends
from sqlmodel import Session, select
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pathlib import Path

from app.database.DataBaseSetup import db_session
from app.database.models import Games
from app.database.models.GameLobby import GameLobbyOnlineUsers, GameInvites, GameInvitationStatus
from app.database.auth import get_current_user

route_game_lobby = APIRouter()

# Setup templates
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_dir)

@route_game_lobby.get("/lobby", response_class=HTMLResponse)
async def game_lobby(request: Request):
    """
    Render the game lobby page
    """
    return templates.TemplateResponse("game_lobby.html", {"request": request})

@route_game_lobby.get("/games", response_model=List[Games])
async def get_available_games(db: Session = Depends(db_session)):
    """Get list of all available games"""
    statement = select(Games).where(Games.available == True)
    games = db.exec(statement).all()
    return games

@route_game_lobby.get("/whos_online/{game}",  response_model=List[GameLobbyOnlineUsers])
async def whos_online(game: int,db: Session = Depends(db_session)):
    """
    Get a list of online users for a specific game
    """
    with logfire.span("whos_online"):
        statement = select(GameLobbyOnlineUsers).where(GameLobbyOnlineUsers.game_id == game)
        users = db.exec(statement).all()
        return users

@route_game_lobby.get("/invites/{game}/{invitee_id}")
async def get_invites(game: int, invitee_id: int, db: Session = Depends(db_session)):
    """
    Get a list of invites for a specific user and game
    """
    with logfire.span("get_invites") as span:
        span.set_attributes(dict(game=game, invitee_id=invitee_id))
        statement = select(GameInvites).where(
            GameInvites.game_id == game,
            GameInvites.invitee_id == invitee_id,
            GameInvites.status == GameInvitationStatus.PENDING
        )
        logfire.info(
            "get_invites",
            game=game,
            invitee_id=invitee_id,
            statement=statement)
        invites = db.exec(statement).all()
        return invites

@route_game_lobby.post("/send_invite/{game}/{user_id}/{invitee_user_id}")
async def send_invite(game: int, user_id: str, invitee_user_id: str):
    """
    Send an invitation to another user
    """
    with logfire.span("send invite") as span:
        span.set_attributes(dict(game=game, user_id=user_id, invitee_user_id=invitee_user_id))
        # This is a placeholder - in a real app, you would send the invite to the database
        return {"status": "success", "message": "Invite sent"}


@route_game_lobby.post("/accept_invite/{invite_id}")
async def accept_invite(invite_id: str):
    """
    Accept an invite and start a game
    """
    # This is a placeholder - in a real app, you would update the invite status in the database
    # and create a new game instance
    return {"status": "success", "message": "Invite accepted", "game_id": "123"}

@route_game_lobby.post("/decline_invite/{invite_id}")
async def decline_invite(invite_id: str):
    """
    Decline an invite
    """
    # This is a placeholder - in a real app, you would update the invite status in the database
    return {"status": "success", "message": "Invite declined"}

@route_game_lobby.get("/current_user")
async def current_user(request: Request, current_user = Depends(get_current_user)):
    """Get the current user's information"""
    return {"user_id": current_user.id, "username": current_user.username}
