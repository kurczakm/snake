import asyncio
import websockets
import json

from game import Player, Game


async def onTurnDone(websocket, game):
    await send_positions(websocket, game)


async def send_positions(websocket, game):
    await websocket.send(json.dumps(game.get_players_info()))


async def send_game_info(websocket, game):
    game_info = {
        'type': 'game_info',
        'width': game.board_width,
        'height': game.board_height
    }
    await websocket.send(json.dumps(game_info))


async def handler(websocket):
    message = await websocket.recv()
    await handle_init_message(websocket, message)


async def handle_init_message(websocket, init_message):
    data = json.loads(init_message)
    if data['action'] == 'start':
        game = Game()
        play_task = asyncio.create_task(game.play(websocket))
        game.start()
        await send_game_info(websocket, game)
        player1 = Player(data['player']['name'], data['player']['color'], [[1, 1]], 'down')
        game.players[player1.name] = player1

        async for message in websocket:
            await handle_message(game, websocket, message)

        await play_task


async def handle_message(game, websocket, message):
    data = json.loads(message)
    print(data)

    match data['action']:
        case 'move':
            player = game.players[data['playerName']]
            direction = data['direction']
            player.setDirection(direction)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
