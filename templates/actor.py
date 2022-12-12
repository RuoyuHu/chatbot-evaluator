from typing import Dict, Any
from enum import Enum


# str mapping, allows for actors to be converted to str
_str_mapping = None

class ActorUninitialisedError(Exception):
    pass

class Actor(Enum):
    """
    Actor Enum for distinct participants in the conversation
    """
    USER=0
    BOT=1

    @staticmethod
    def initialise_mapping(mappings: Dict[Any, str]) -> None:
        # Set str mapping, needs to be called in order to convert object to str
        global _str_mapping
        _str_mapping = mappings

    def __str__(self) -> str:
        global _str_mapping
        if _str_mapping is None:
            raise ActorUninitialisedError("Actor.str_mapping needs to be initialised for printing")

        return _str_mapping[self]
