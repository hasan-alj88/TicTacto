from decouple import config
from fastapi import FastAPI
from routes.RouteTicTacToe import route_tictactoe
import logfire

app = FastAPI()

logfire.configure(
    token=config('LOGFIRE_TOKEN'),
    service_name=config('LOGFIRE_SERVICE_NAME'),
    environment=config('LOGFIRE_ENVIRONMENT', default='dev'),
    data_dir='logs'
)
logfire.instrument_fastapi(app)


app.include_router(route_tictactoe, prefix='/tictactoe', tags=['TicTacToe'])