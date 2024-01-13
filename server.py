import asyncio
import websockets
import json

from game import BOARD_WIDTH, BOARD_HEIGHT, Player, players, play, get_players_info, start, result


class Server:
    def __init__(self, websocket):
        self.websocket = websocket

    async def onTurnDone(self):
        await self.send_positions()

    async def send_positions(self):
        await self.websocket.send(json.dumps(get_players_info()))

    async def send_game_info(self):
        game_info = {
            'type': 'game_info',
            'width': BOARD_WIDTH,
            'height': BOARD_HEIGHT
        }
        await self.websocket.send(json.dumps(game_info))

    async def handler(self):
        play_task = asyncio.create_task(play(self))

        async for message in self.websocket:
            await self.handle_message(message)

        await play_task

    async def handle_message(self, message):
        data = json.loads(message)
        print(data)

        match data['action']:
            case 'start':
                start()
                await self.send_game_info()
                player1 = Player(data['player']['name'], data['player']['color'], [[1, 1]], 'down')
                players[player1.name] = player1
            case 'move':
                player = players[data['playerName']]
                direction = data['direction']
                player.setDirection(direction)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


async def handler(websocket):
    server = Server(websocket)
    await server.handler()


if __name__ == '__main__':
    asyncio.run(main())
