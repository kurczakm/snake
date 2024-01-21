class State:
    WAITING_FOR_ANOTHER_PLAYER = 'WAITING_FOR_ANOTHER_PLAYER'
    GAME_OVER = 'GAME_OVER'
    GAME_IN_PROGRESS = 'GAME_IN_PROGRESS'


class Direction:
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    UP = 'up'


class Action:
    START = 'start'
    JOIN = 'join'
    MOVE = 'move'


class MessageType:
    GAME_INFO = 'game_info'
    ERROR = 'error'
    STATUS = 'status'
