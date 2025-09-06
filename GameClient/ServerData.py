from nicegui import ui


def get_game():
    games_dict = {
     11:
        {
        "GameName": "TicTacToe",
        "GameIMG":'Static/Images/TicTacToeImage.png'
    },
    12:
        {
        "GameName": "Blackjack",
        "GameIMG":'Static/Images/blackjack.png'
    },
    13:
        {
        "GameName": "Rock Paper Scissors Lizard Spock",
        "GameIMG": 'Static/Images/rock-paper-scissors.png'
    }
    }

    return games_dict


def get_online_players_data(gameid: int):
    people_online = {1:"Testing",2:"Dummy",3:"Dummy2"}

    if gameid == 13:
        return   {112:"test_dummy",205:"test_dummy2",3345:"test_dummy3"}

    if gameid == 12:
        return   {7:"player1",234:"player2",312:"player3"}

    if gameid == 11:
        return people_online

def get_invites_data(gameid: int):
    if gameid == 11:
        return {1:"Testing",2:"Dummy",3:"Dummy2"}
    if gameid == 12:
        return {5:"Testing2",7:"testing7",8:"dummy6"}
    if gameid == 13:
        return {9: "Test_dummy1",10:"Test_dummy2",11:"Test_dummy3"}

def player_online_entry(player_name: str, player_id : int, game_eyed : int):
    with ui.row():
        ui.label(f'{player_name}')
        ui.button('Invite', on_click= lambda: send_game_invite(player_name,player_id,game_eyed))

def send_game_invite(player_name: str, player_id : int, game_eyed : int):
    ui.notify(f'{player_name, player_id} invited to {game_eyed}')

def accept_invite(player_name: str, player_id : int, game_eyed : int):
    with ui.row():
        ui.label(f'{player_name}')
        ui.button('Accept Invite', on_click= lambda: accepted_invite(player_name,player_id,game_eyed))

def accepted_invite(player_name: str, player_id : int, game_eyed : int):
    ui.notify(f'{player_name, player_id} accepted a game to {game_eyed}')



@ui.page('/GameLobby/{GameID}')
def game_lobby_page(GameID: int):
    ui.label(f'Welcome to the lobby {GameID}')
    with ui.list().props('bordered separator'):
        ui.item_label('Online Players').props('header').classes('text-bold')
        ui.separator()
        for player_id,player_name in get_online_players_data(GameID).items():
            player_online_entry(game_eyed=GameID,
                                player_id=player_id,
                                player_name=player_name)

    with ui.list().props('bordered separator'):
        ui.item_label('Invites').props('header').classes('text-bold')
        ui.separator()
        for player_eyed,players_name in get_invites_data(GameID).items():
            accept_invite(game_eyed=GameID,
                          player_id=player_eyed,
                          player_name= players_name )
def game_card(game_eyed : int, game_name :str, game_img : str):
    with ui.card():
        ui.label(f'{game_name}')
        ui.image(f'{game_img}').classes('w-64')
        ui.button('GameLobby', on_click=lambda: ui.navigate.to(f'/GameLobby/{game_eyed}'))


with ui.row().classes('flex-wrap justify-center gap-4',):
    for game_id , game_info in get_game().items():
        game_card(game_id, game_info["GameName"], game_info["GameIMG"])





ui.run()