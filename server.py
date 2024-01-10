import asyncio
import websockets
import json

from game import BOARD_WIDTH, BOARD_HEIGHT, Player, players


async def handler(websocket):
    print('Game initialized')

    async for message in websocket:
        await handle_message(message, websocket)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


async def handle_message(message, websocket):
    data = json.loads(message)
    print(data)

    match data['action']:
        case 'start':
            await send_game_info(websocket)
            player1 = Player(data['player']['name'], data['player']['color'], [[1, 1]])
            players[player1.name] = player1
        case 'move':
            player = players[data['playerName']]
            direction = data['direction']
            player.move(direction)
            await send_position(websocket, player)


async def send_game_info(websocket):
    game_info = {
        'type': 'game_info',
        'width': BOARD_WIDTH,
        'height': BOARD_HEIGHT
    }
    await websocket.send(json.dumps(game_info))


async def send_position(websocket, player):
    await websocket.send(json.dumps(player.get_player_info()))


if __name__ == '__main__':
    asyncio.run(main())
