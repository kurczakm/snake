import asyncio
import websockets
import json

BOARD_WIDTH = 10
BOARD_HEIGHT = 10

POSITION = [0, 0]

INFO = {
    'type': 'positions',
    'players': [
        {
            'name': 'player1',
            'color': 'blue',
            'head': POSITION
        }
    ]
}


async def handler(websocket):
    print('Game initialized')

    async for message in websocket:
        await handleMessage(message, websocket)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


async def handleMessage(message, websocket):
    data = json.loads(message)
    print(data)

    match data['action']:
        case 'start':
            await sendGameInfo(websocket)
        case 'move':
            move(data['direction'])
            await sendPostion(websocket)


def move(direction):
    match direction:
        case 'left':
            if (POSITION[0] > 0):
                POSITION[0] = POSITION[0] - 1
        case 'right':
            if (POSITION[0] < BOARD_WIDTH - 1):
                POSITION[0] = POSITION[0] + 1
        case 'up':
            if (POSITION[1] > 0):
                POSITION[1] = POSITION[1] - 1
        case 'down':
            if (POSITION[1] < BOARD_HEIGHT - 1):
                POSITION[1] = POSITION[1] + 1



async def sendGameInfo(websocket):
    gameInfo = {
        'type': 'game_info',
        'width': BOARD_WIDTH,
        'height': BOARD_HEIGHT
    }
    await websocket.send(json.dumps(gameInfo))


async def sendPostion(websocket):
    await websocket.send(json.dumps(INFO))


if __name__ == '__main__':
    asyncio.run(main())
