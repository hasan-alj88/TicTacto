from contextlib import asynccontextmanager
from pathlib import Path
from decouple import config
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.routes.RouteTicTacToe import route_tictactoe
from app.routes.RouteAuthentication import route_authentication
from app.database.DataBaseSetup import create_db_and_tables
import logfire

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
async def lifespan(app: FastAPI):
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

app.include_router(route_tictactoe, prefix='/tictactoe', tags=['TicTacToe'])
app.include_router(route_authentication, prefix='/auth', tags=['Authentication'])