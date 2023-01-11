import os
import json

from typing import Dict, List, Any

from utils.parsing import parse_conversation
from utils.loader import load_dialog
from templates.actor import Actor

from example.utterance import ExampleUtterance
from example.evaluator import ExampleEvaluator
from example.chatbot import ExampleChatbotWrapper


# Actor names for logging/printing purposes
# Used to initialise Actor names
actor_names = {
    Actor.USER: "USER",
    Actor.BOT: "BOT"
}

def _example_end_conv_func(context: List[ExampleUtterance]) -> bool:
    """
    Example function for determining if the conversation is over, used when
    evaluating a chatbot.

    i.e. This could refer to when either responses contain 'bye'

    :param List[ExampleUtterance] context: Conversation as context
    """
    return len(context) > 5


def main(global_config: Dict[str, Any], *args, **kwargs):

    if 'mode' not in global_config:
        raise AttributeError("Evaluation Mode Not Specified!")

    # Assuming user is calling program entry point at root
    module_dir = os.path.join(os.curdir, global_config['target_dir'])

    # Attempt to load and set local config
    local_config = {}
    local_config_dir = os.path.join(module_dir, 'config.json')
    if os.path.isfile(local_config_dir):
        local_config = json.load(open(local_config_dir))

    # Allow local config to know where it is
    local_config['local_dir'] = global_config['target_dir']

    # Initialise actor Enum -> str mappings
    Actor.initialise_mapping(mappings=actor_names)

    # Instantiate evaluator with local config
    evaluator = ExampleEvaluator(config=local_config)

    if global_config['mode'] == 'c':
        # perform interactive evaluation of a chatbot
        evaluator.score_chatbot(chatbot=ExampleChatbotWrapper(), condition=_example_end_conv_func)

    if global_config['mode'] == 'd':
        # perform document level evaluation
        if 'eval_target' not in local_config:
            # Evaluation on a document/conversation trascript must have an 'eval_target' specified
            raise AttributeError("No Evaluation Target Specified!")

        # Load utterances from document
        target_path = os.path.join(module_dir, local_config['eval_target'])
        eval_targets = load_dialog(target=target_path)
        for (target_path, target_name) in eval_targets:
            print(f"Evaluating conversation in {repr(target_name)}")
            eval_target = open(target_path, 'r')
            eval_target = eval_target.read().splitlines()

            # Parse utterances/conversation into ExampleUtterance objects
            example_conv = parse_conversation(conversation=eval_target, actors=Actor, wrapper=ExampleUtterance)
            conv_score = evaluator.score_document(document=example_conv)
            print(f"Score of conversation in {target_name} is: {conv_score}")
