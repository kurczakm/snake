import asyncio
import secrets

import websockets
import json

from game import Game
from constants import Action, MessageType

JOIN = {}


async def on_turn_done(game, connected):
    await send_positions(game, connected)


async def send_positions(game, connected):
    for websocket in connected:
        await websocket.send(json.dumps(game.get_players_info()))


async def send_game_info(websocket, game, join_key):
    game_info = {
        'type': MessageType.GAME_INFO,
        'width': game.board_width,
        'height': game.board_height,
        'key': join_key
    }
    await websocket.send(json.dumps(game_info))


async def handler(websocket):
    message = await websocket.recv()
    await handle_init_message(websocket, message)


async def handle_init_message(websocket, init_message):
    data = json.loads(init_message)
    if data['action'] == Action.START:
        await start(websocket, data)
    if data['action'] == Action.JOIN:
        await join(websocket, data)


async def start(websocket, data):
    game = Game()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        await send_game_info(websocket, game, join_key)
        game.add_player(data['player']['name'])
        await send_positions(game, connected)
        async for message in websocket:
            await handle_message(game, websocket, message)
    finally:
        del JOIN[join_key]


async def error(websocket, message):
    event = {
        'type': MessageType.ERROR,
        'message': message
    }
    await websocket.send(json.dumps(event))


async def join(websocket, data):
    try:
        join_key = data['key']
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, 'Game not found')
        return

    connected.add(websocket)

    try:
        await send_game_info(websocket, game, join_key)
        game.add_player(data['player']['name'])
        await send_positions(game, connected)

        play_task = asyncio.create_task(game.play(connected))
        game.start()

        async for message in websocket:
            await handle_message(game, websocket, message)

        await play_task
    finally:
        connected.remove(websocket)


async def handle_message(game, websocket, message):
    data = json.loads(message)

    match data['action']:
        case Action.MOVE:
            player = game.players[data['playerName']]
            direction = data['direction']
            player.setDirection(direction)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
