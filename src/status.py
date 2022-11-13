from enum import Enum, auto, unique


@unique
class Status(Enum):
    SUCCESS = auto()
    GREP_FAILURE = auto()
    COMPILE_FAILURE = auto()
    EXECUTION_FAILURE = auto()
    COMPARING_FAILURE = auto()
