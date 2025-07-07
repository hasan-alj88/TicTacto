from typing import List

import logfire
from fastapi import (APIRouter, Request, Depends, HTTPException, status)
from sqlmodel import Session, select
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pathlib import Path

from app.Auth import user_dependency, db_dependency
from app.DataModels.GameLobbyData import GameInfoData
from app.database.DataBaseSetup import db_session
from app.database.models import GameLobbyOnlineUsers, GameInvites, GameInvitationStatus, Games

route_game_lobby = APIRouter()

# Setup templates
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_dir)


# @route_game_lobby.get("/games")
# async def get_available_games(db: Session = db_dependency)->List[GameInfoData]:
#     """Get list of all available games"""
#     statement = select(Games).where(Games.available == True)
#     games = db.exec(statement).all()
#     game_list = []
#     for game in games:
#         game_list.append(GameInfoData(
#             game_name=game.name,
#             game_description=game.description,
#             is_game_available=game.available,
#             game_icon=game.icon,
#         )
#         )
#     return game_list


@route_game_lobby.get("/lobby/{game_name}/{user_name}", response_class=HTMLResponse)
async def game_lobby(
        request: Request,
        user_name: str,
        game_name: str,
        current_user: user_dependency  # This requires authentication
):
    """
    Render the game lobby page - only accessible by the authenticated user
    """
    with logfire.span("game lobby"):
        if current_user.username != user_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own lobby"
            )
        return templates.TemplateResponse(
            "game_lobby.html",
            {
                "request": request,
                "game_name": game_name,
                "username": user_name,
                "user": current_user
            }
        )


@route_game_lobby.get("/whos_online/{game}",  response_model=List[GameLobbyOnlineUsers])
async def whos_online(game: int,db: db_dependency, current_user: user_dependency):
    """
    Get a list of online users for a specific game
    """
    with logfire.span("whos_online"):
        statement = select(GameLobbyOnlineUsers).where(
            GameLobbyOnlineUsers.game_id == game).where(
            GameLobbyOnlineUsers.user_id != current_user.id
        )
        users = db.exec(statement).all()
        return users

@route_game_lobby.put("/go_online/{game}/{username}")
async def go_online(game: str, username: str, db: db_dependency, current_user: user_dependency)->bool:
    with logfire.span("go online", username=username, game=game):
        if username != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own lobby"
            )
        game_id = select(Games.id).where(Games.name == game)
        game_id = db.exec(game_id).first()
        # check if user is already online
        statement = select(GameLobbyOnlineUsers).where(
            GameLobbyOnlineUsers.game_id == game_id,
            GameLobbyOnlineUsers.user_id == current_user.id
        )
        if db.exec(statement).first():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You are already online"
            )

        record = GameLobbyOnlineUsers(game_id=game, user_id=current_user.id, username=username)
        db.add(record)
        db.commit()
        db.refresh(record)
        return True

@route_game_lobby.put("/go_offline/{game}/{username}")
async def go_offline(game: str, username: str, db: db_dependency, current_user: user_dependency) -> bool:
    with logfire.span("go offline", username=username, game=game):
        if username != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own lobby"
            )
        game_id = select(Games.id).where(Games.name == game)
        game_id = db.exec(game_id).first()

        # check if user is already offline
        record = db.exec(select(GameLobbyOnlineUsers).where(
            GameLobbyOnlineUsers.game_id == game_id,
            GameLobbyOnlineUsers.user_id == current_user.id
        )).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You are already offline"
            )



@route_game_lobby.get("/invites/{game}/{invitee_id}")
async def get_invites(game: str, invitee_id: int, db: Session = Depends(db_session)):
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
