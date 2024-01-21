import asyncio
import random


class Game:
    def __init__(self):
        self.board_width = 10
        self.board_height = 10
        self.tick = 0.4
        self.players = {}
        self.started = False
        self.food = []
        self.result = 'IN_PROGRESS'

    async def play(self, websocket):
        from server import onTurnDone

        while True:
            if self.started:
                self.next_turn()
                await onTurnDone(websocket, self)
            await asyncio.sleep(self.tick)

    def next_turn(self):
        for playerName in self.players:
            player = self.players[playerName]
            player.last_direction = player.direction
            food_eaten = player.move(self.food)
            if food_eaten:
                self.add_food()

        self.check_collisions()

    def check_collisions(self):
        for playerName in self.players:
            player = self.players[playerName]
            head = player.body_segments[0]

            if head[0] < 0 or head[0] > self.board_width or head[1] < 0 or head[1] > self.board_height:
                self.started = False
                self.result = 'GAME_OVER'
                return

            for playerName2 in self.players:
                player2 = self.players[playerName2]

                for index, segment in enumerate(player2.body_segments):
                    if playerName2 == playerName and index == 0:
                        continue

                    if segment == head:
                        self.started = False
                        self.result = 'GAME_OVER'
                        return

    def get_players_info(self):
        players_info = []
        for playerName in self.players:
            player = self.players[playerName]
            players_info.append({
                'name': player.name,
                'color': player.color,
                'bodySegments': player.body_segments
            })

        return {
            'type': 'status',
            'food': self.food,
            'players': players_info,
            'gameResult': self.result
        }

    def add_food(self):
        x_candidates = list(range(0, self.board_width))
        y_candidates = list(range(0, self.board_height))

        for playerName in self.players:
            player = self.players[playerName]
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

        self.food.append([x, y])

    def start(self):
        self.food = []
        self.add_food()
        self.started = True


class Player:
    def __init__(self, name, color, body_segments, direction):
        self.name = name
        self.color = color
        self.body_segments = body_segments
        self.direction = direction
        self.last_direction = direction

    def move(self, food):
        x, y = self.body_segments[0]
        match self.direction:
            case 'left':
                x = x - 1
            case 'right':
                x = x + 1
            case 'up':
                y = y - 1
            case 'down':
                y = y + 1
        self.body_segments.insert(0, [x, y])

        food_eaten = -1
        try:
            food_eaten = food.index([x, y])
        except ValueError:
            pass

        if food_eaten == -1:
            del self.body_segments[-1]
            return False
        else:
            del food[food_eaten]
            return True

    def setDirection(self, direction):
        if direction == 'up' and self.last_direction == 'down':
            return

        if direction == 'left' and self.last_direction == 'right':
            return

        if direction == 'down' and self.last_direction == 'up':
            return

        if direction == 'right' and self.last_direction == 'left':
            return

        self.direction = direction
