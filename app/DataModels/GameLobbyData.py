from pydantic import BaseModel


class GameInfoData(BaseModel):
    game_name: str
    game_description: str
    is_game_available: bool
    game_icon: str