import asyncio

BOARD_WIDTH = 10
BOARD_HEIGHT = 10
TICK = 0.4
players = {}
started = False


async def play(server):
    while True:
        if started:
            next_turn()
            await server.onTurnDone()
        await asyncio.sleep(TICK)


def next_turn():
    for playerName in players:
        player = players[playerName]
        player.move()


def get_players_info():
    players_info = []
    for playerName in players:
        player = players[playerName]
        players_info.append({
            'name': player.name,
            'color': player.color,
            'bodySegments': player.body_segments
        })

    return {
        'type': 'players_info',
        'players': players_info
    }


def start():
    global started
    started = True


class Player:
    def __init__(self, name, color, body_segments, direction):
        self.name = name
        self.color = color
        self.body_segments = body_segments
        self.direction = direction

    def move(self):
        x, y = self.body_segments[0]
        match self.direction:
            case 'left':
                if x > 0:
                    x = x - 1
            case 'right':
                if x < BOARD_WIDTH - 1:
                    x = x + 1
            case 'up':
                if y > 0:
                    y = y - 1
            case 'down':
                if y < BOARD_HEIGHT - 1:
                    y = y + 1
        self.body_segments.insert(0, [x, y])
        del self.body_segments[-1]

    def setDirection(self, direction):
        self.direction = direction
