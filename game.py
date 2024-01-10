BOARD_WIDTH = 10
BOARD_HEIGHT = 10
players = {}


class Player:
    def __init__(self, name, color, body_segments):
        self.name = name
        self.color = color
        self.body_segments = body_segments

    def move(self, direction):
        x, y = self.body_segments[0]
        match direction:
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

    def get_player_info(self):
        return {
            'type': 'player_info',
            'players': [
                {
                    'name': self.name,
                    'color': self.color,
                    'bodySegments': self.body_segments
                }
            ]
        }
