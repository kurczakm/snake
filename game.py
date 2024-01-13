import asyncio
import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 10
TICK = 0.4
players = {}
started = False
food = []


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
        'type': 'status',
        'food': food,
        'players': players_info
    }


def add_food():
    x_candidates = list(range(0, BOARD_WIDTH))
    y_candidates = list(range(0, BOARD_HEIGHT))

    for playerName in players:
        player = players[playerName]
        for segment in player.body_segments:
            try:
                x_candidates.remove(segment[0])
            except ValueError:
                pass
            try:
                y_candidates.remove(segment[1])
            except ValueError:
                pass

    x = random.choice(x_candidates)
    y = random.choice(y_candidates)

    food.append([x, y])


def start():
    add_food()
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

        food_eaten = -1
        try:
            food_eaten = food.index([x, y])
        except ValueError:
            pass

        if food_eaten == -1:
            del self.body_segments[-1]
        else:
            del food[food_eaten]
            add_food()

    def setDirection(self, direction):
        self.direction = direction
