from enum import Enum


class AgentType(Enum):
    HUMAN = 1
    PASSIVE = 2
    AGGRESSIVE = 3
    PACIFIST = 4
    GREEDY = 5


class GamePlayId(Enum):
    P1 = 1
    P2 = 2
    NONE = 3

class GameStatus(Enum):
    ONGOING = 1
    ENDED = 2


class PlayerAction(Enum):
    DEPLOY = 1
    MARCH = 2
    INVADE = 3