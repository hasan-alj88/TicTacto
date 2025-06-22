import logfire
from fastapi import APIRouter

route_tictactoe = APIRouter()

@route_tictactoe.get("/")
async def root():
    logfire.info("Hello World")
    return {"message": "Hello World"}