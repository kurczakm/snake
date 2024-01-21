import asyncio
import random
from constants import State, Direction, MessageType


class Game:
    def __init__(self):
        self.board_width = 10
        self.board_height = 10
        self.tick = 3
        self.players = {}
        self.started = False
        self.food = []
        self.state = State.WAITING_FOR_ANOTHER_PLAYER

    async def play(self, connected):
        from server import on_turn_done

        while True:
            if self.started:
                self.next_turn()
                await on_turn_done(self, connected)
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

            if head[0] < 0 or head[0] >= self.board_width or head[1] < 0 or head[1] >= self.board_height:
                self.started = False
                self.state = State.GAME_OVER
                return

            for playerName2 in self.players:
                player2 = self.players[playerName2]

                for index, segment in enumerate(player2.body_segments):
                    if playerName2 == playerName and index == 0:
                        continue

                    if segment == head:
                        self.started = False
                        self.state = State.GAME_OVER
                        return

    def get_players_info(self):
        players_info = []
        for playerName in self.players:
            player = self.players[playerName]
            players_info.append({
                'name': player.name,
                'bodySegments': player.body_segments
            })

        return {
            'type': MessageType.STATUS,
            'food': self.food,
            'players': players_info,
            'state': self.state
        }

    def add_player(self, name):
        x, y = self.get_random_free_coordinate()
        player = Player(name, [[x, y]], Direction.DOWN)
        self.players[player.name] = player

    def get_random_free_coordinate(self):
        x_candidates = list(range(0, self.board_width))
        y_candidates = list(range(0, self.board_height))

        for playerName in self.players:
            player = self.players[playerName]
            for segment in player.body_segments:
                remove_coordinate(x_candidates, y_candidates, segment)

        for food in self.food:
            remove_coordinate(x_candidates, y_candidates, food)

        x = random.choice(x_candidates)
        y = random.choice(y_candidates)

        return x, y

    def add_food(self):
        x, y = self.get_random_free_coordinate()
        self.food.append([x, y])

    def start(self):
        self.food = []
        self.add_food()
        self.started = True
        self.state = State.GAME_IN_PROGRESS


class Player:
    def __init__(self, name, body_segments, direction):
        self.name = name
        self.body_segments = body_segments
        self.direction = direction
        self.last_direction = direction

    def move(self, food):
        x, y = self.body_segments[0]
        match self.direction:
            case Direction.LEFT:
                x = x - 1
            case Direction.RIGHT:
                x = x + 1
            case Direction.UP:
                y = y - 1
            case Direction.DOWN:
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
        if direction == Direction.UP and self.last_direction == Direction.DOWN:
            return

        if direction == Direction.LEFT and self.last_direction == Direction.RIGHT:
            return

        if direction == Direction.DOWN and self.last_direction == Direction.UP:
            return

        if direction == Direction.RIGHT and self.last_direction == Direction.LEFT:
            return

        self.direction = direction


def remove_coordinate(x_candidates, y_candidates, coordinate):
    try:
        x_candidates.remove(coordinate[0])
    except ValueError:
        pass
    try:
        y_candidates.remove(coordinate[1])
    except ValueError:
        pass
