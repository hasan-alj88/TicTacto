import logfire
import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.DataBaseSetup import db_session
from app.database.models.TicTacToGame import TicTacToeGames, TicTacToeMoveHistory
from app.database.models import User

route_tictactoe = APIRouter()

@route_tictactoe.get("/")
async def root():
    logfire.info("Hello World")
    return {"message": "Hello World"}


@route_tictactoe.get("/tictactoe/new_game/{player_1}/{player_2}")
async def new_game(player_1: int, player_2: int, db: Session = Depends(db_session)):
    logfire.info("New TicTacTo game started")
    player_1, player_2 = np.random.choice([player_1, player_2], size=2, replace=False)
    logfire.info(f"Players selected: {player_1} and {player_2}")

    new_game_record = TicTacToeGames(player_one_id=player_1, player_two_id=player_2)
    db.add(new_game_record)
    db.commit()
    db.refresh(new_game_record)

    return {"game_id": new_game_record.id}

@route_tictactoe.get("/game/{game_id}")
async def get_game(game_id: int, db: Session = Depends(db_session)):
    """
    Get the current state of a game
    """
    # Get the game
    game = db.get(TicTacToeGames, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get the players
    player_one = db.get(User, game.player_one_id)
    player_two = db.get(User, game.player_two_id)

    # Get the moves
    statement = select(TicTacToeMoveHistory).where(TicTacToeMoveHistory.game_id == game_id)
    moves = db.exec(statement).all()

    # Create the board
    board = np.zeros((3, 3), dtype=int)
    for move in moves:
        # Player one is 1, player two is 2
        player_value = 1 if move.player_id == game.player_one_id else 2
        board[move.row, move.col] = player_value

    # Determine current player
    current_player = 1 if len(moves) % 2 == 0 else 2

    # Check for winner
    winner = None
    game_over = False

    # Check rows
    for row in range(3):
        if board[row, 0] != 0 and board[row, 0] == board[row, 1] == board[row, 2]:
            winner = board[row, 0]
            game_over = True

    # Check columns
    for col in range(3):
        if board[0, col] != 0 and board[0, col] == board[1, col] == board[2, col]:
            winner = board[0, col]
            game_over = True

    # Check diagonals
    if board[0, 0] != 0 and board[0, 0] == board[1, 1] == board[2, 2]:
        winner = board[0, 0]
        game_over = True
    if board[0, 2] != 0 and board[0, 2] == board[1, 1] == board[2, 0]:
        winner = board[0, 2]
        game_over = True

    # Check if board is full (draw)
    if np.all(board != 0):
        game_over = True
        if winner is None:
            winner = 0  # Draw

    return {
        "game_id": game.id,
        "player_one_id": game.player_one_id,
        "player_one_username": player_one.username,
        "player_two_id": game.player_two_id,
        "player_two_username": player_two.username,
        "board": board.tolist(),
        "current_player": current_player,
        "game_over": game_over,
        "winner": winner
    }

@route_tictactoe.post("/move/{game_id}")
async def make_move(game_id: int, move: dict, db: Session = Depends(db_session)):
    """
    Make a move in the game
    """
    # Get the game
    game = db.get(TicTacToeGames, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Validate the move
    row = move.get("row")
    col = move.get("col")
    player_id = move.get("player_id")

    if row is None or col is None or player_id is None:
        raise HTTPException(status_code=400, detail="Invalid move data")

    if row < 0 or row > 2 or col < 0 or col > 2:
        raise HTTPException(status_code=400, detail="Invalid move position")

    if player_id != game.player_one_id and player_id != game.player_two_id:
        raise HTTPException(status_code=400, detail="Player not in this game")

    # Get the moves
    statement = select(TicTacToeMoveHistory).where(TicTacToeMoveHistory.game_id == game_id)
    moves = db.exec(statement).all()

    # Create the board
    board = np.zeros((3, 3), dtype=int)
    for m in moves:
        player_value = 1 if m.player_id == game.player_one_id else 2
        board[m.row, m.col] = player_value

    # Check if the cell is already occupied
    if board[row, col] != 0:
        raise HTTPException(status_code=400, detail="Cell already occupied")

    # Determine current player
    current_player = 1 if len(moves) % 2 == 0 else 2
    expected_player_id = game.player_one_id if current_player == 1 else game.player_two_id

    # Check if it's the player's turn
    if player_id != expected_player_id:
        raise HTTPException(status_code=400, detail="Not your turn")

    # Make the move
    new_move = TicTacToeMoveHistory(
        game_id=game_id,
        player_id=player_id,
        row=row,
        col=col
    )
    db.add(new_move)
    db.commit()

    # Update the board
    player_value = 1 if player_id == game.player_one_id else 2
    board[row, col] = player_value

    # Check for winner
    winner = None
    game_over = False

    # Check rows
    for r in range(3):
        if board[r, 0] != 0 and board[r, 0] == board[r, 1] == board[r, 2]:
            winner = board[r, 0]
            game_over = True

    # Check columns
    for c in range(3):
        if board[0, c] != 0 and board[0, c] == board[1, c] == board[2, c]:
            winner = board[0, c]
            game_over = True

    # Check diagonals
    if board[0, 0] != 0 and board[0, 0] == board[1, 1] == board[2, 2]:
        winner = board[0, 0]
        game_over = True
    if board[0, 2] != 0 and board[0, 2] == board[1, 1] == board[2, 0]:
        winner = board[0, 2]
        game_over = True

    # Check if board is full (draw)
    if np.all(board != 0):
        game_over = True
        if winner is None:
            winner = 0  # Draw

    # Update game turn
    game.turn = game.turn + 1
    db.add(game)
    db.commit()

    return {
        "success": True,
        "board": board.tolist(),
        "current_player": 2 if current_player == 1 else 1,  # Switch player
        "game_over": game_over,
        "winner": winner
    }
