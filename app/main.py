from contextlib import asynccontextmanager
from pathlib import Path

import logfire
from decouple import config
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.database.DataBaseSetup import create_db_and_tables
from app.routes import (route_tictactoe, route_authentication, route_game_lobby)

load_dotenv()

logfire.configure(
    token=config('LOGFIRE_TOKEN'),
    service_name=config('LOGFIRE_SERVICE_NAME'),
    environment=config('LOGFIRE_ENVIRONMENT', default='dev'),
    data_dir='logs'
)

logfire.instrument_sqlalchemy()
logfire.instrument_requests()
logfire.instrument_sqlite3()

@asynccontextmanager
async def lifespan(app: FastAPI): # noqa : ARG001
    with logfire.span("Game APP Run"):
        create_db_and_tables()
        yield
app = FastAPI(lifespan=lifespan)

logfire.instrument_fastapi(app)
logfire.instrument_starlette(app)
# Setup templates and static files
templates_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"

templates = Jinja2Templates(directory=templates_dir)
app.mount(str(static_dir), StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def home_page():
    return FileResponse(static_dir/'home.html')

@app.get("/register")
async def register_page():
    return FileResponse(static_dir/'registration.html')


app.include_router(route_authentication, prefix='/auth', tags=['Authentication'])
app.include_router(route_game_lobby, prefix='/game_lobby', tags=['GameLobby'])
app.include_router(route_tictactoe, prefix='/tictactoe', tags=['TicTacToe'])