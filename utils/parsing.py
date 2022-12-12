from typing import List, Dict, TextIO
from enum import Enum

from templates.utterance import BaseUtterance
from templates.actor import Actor
from utils.keywords import delims


def parse_line(line: str, actors: Dict[str, Actor], wrapper: type) -> BaseUtterance:
    # Applies parsing to a single utterance, produces a utterance object
    [actor, text] = line.split(delims.CONV_SEP)
    if actor not in actors:
        raise AttributeError(f"Invalid Actor Detected from transcript: {repr(actor)} not in actors!")

    return wrapper(actor=actors[actor], text=text)


def parse_conversation(conversation: List[str], actors: Enum, wrapper: type) -> List[BaseUtterance]:
    """
    Parser helper function to aid in loading conversations

    :param List[str]    conversation: List of utterances in str format
    :param Enum         actors: Actor enums known to the system
    :param type         wrapper: A type obj, MUST BE child of BaseUtterance

    :return:            List of utterances as utterance objects
    """
    actor_names = [str(actor) for actor in actors]
    mapper = dict(list(zip(actor_names, actors)))
    return [parse_line(line=line, actors=mapper, wrapper=wrapper) for line in conversation]


def save_conversation(stream: TextIO, conversation: List[BaseUtterance], mapper: Dict=None) -> None:
    """
    Helper function to save a given conversation to a text file in a parser-specific format

    :param TextIO               stream: Opened output stream/file object
    :param List[BaseUtterance]  conversation: Conversation to save
    :param Dict                 mapper: Optional argument for custom name mappings
    """
    if mapper is not None:
        actor_mapping = lambda a: mapper[a]
    else:
        actor_mapping = lambda a: str(a)

    str_conv = []
    for line in conversation:
        str_actor = actor_mapping(line.actor)
        str_output = str_actor + delims.CONV_SEP + line.text
        str_conv.append(str_output)

    stream.write('\n'.join(str_conv))
