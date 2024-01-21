import asyncio
import websockets
import json

from game import BOARD_WIDTH, BOARD_HEIGHT, Player, players, play, get_players_info, start, result


async def onTurnDone(websocket):
    await send_positions(websocket)


async def send_positions(websocket):
    await websocket.send(json.dumps(get_players_info()))


async def send_game_info(websocket):
    game_info = {
        'type': 'game_info',
        'width': BOARD_WIDTH,
        'height': BOARD_HEIGHT
    }
    await websocket.send(json.dumps(game_info))


async def handler(websocket):
    play_task = asyncio.create_task(play(websocket))

    async for message in websocket:
        await handle_message(websocket, message)

    await play_task


async def handle_message(websocket, message):
    data = json.loads(message)
    print(data)

    match data['action']:
        case 'start':
            start()
            await send_game_info(websocket)
            player1 = Player(data['player']['name'], data['player']['color'], [[1, 1]], 'down')
            players[player1.name] = player1
        case 'move':
            player = players[data['playerName']]
            direction = data['direction']
            player.setDirection(direction)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
