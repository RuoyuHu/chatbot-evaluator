from typing import List

from templates.utterance import BaseUtterance
from templates.actor import Actor


class BaseChatbot:
    """
    Template chatbot class, used to produce wrappers for generating utterances
    """

    def respond(self, context: List[BaseUtterance], actor: Actor, **kwargs) -> BaseUtterance:
        """
        Produce a contextual response based on speaker and previous conversation

        :param List[BaseUtterance]  context: Conversation context, previous conversation
        :param Actor                actor: Current speaker in the conversation

        :return: Generated response
        :rtype: BaseUtterance
        """
        raise NotImplementedError
