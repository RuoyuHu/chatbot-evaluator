from typing import List

from example.utterance import ExampleUtterance
from templates.chatbot import BaseChatbot
from templates.actor import Actor

class ExampleChatbotBackend:
    """
    Example of conversation backend, this could be any means of generating
    responses, i.e. pre-trained generation, retrieval, loading etc.

    A wrapper can be applied to this response generator and used in evaluation
    """
    @staticmethod
    def custom_function(context: List[str]) -> str:
        return f"This is utterance {len(context)}"


class ExampleChatbotWrapper(BaseChatbot):
    """
    Example wrapper around chatbot object

    Fetches chatbot/generator responses and formats it to fit the required type
    signature
    """

    def respond(self, context: List[ExampleUtterance], actor: Actor, **kwargs) -> ExampleUtterance:
        prev_utterances = [utt.text for utt in context]
        generated_response = ExampleChatbotBackend.custom_function(context=prev_utterances)
        return ExampleUtterance(actor=actor, text=generated_response)
