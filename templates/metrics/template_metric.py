from typing import List
from templates.utterance import BaseUtterance

class BaseEvalMetric:
    """
    Template evaluation metric class
    """

    def score_utterance(self, utterance: BaseUtterance, context: List[BaseUtterance], **kwargs) -> float:
        """
        Scoring function, all evaluation metrics should be able to take an
        utterance, a context and any additional required information and
        produce a score of the given utterance

        :param BaseUtterance  utterance: Given utterance to evaluate
        :param BaseUtterance  context: The context to evaluate the utterance

        :return: Evaluation score of the given utterance in the context
        :rtype: float
        """
        raise NotImplementedError

    def score_conversation(self, conversation: List[BaseUtterance], **kwargs) -> float:
        """
        Scoring function, for metrics that are applied at the conversation level
        rather than the turn level

        :param List[BaseUtterance]  conversation: Full conversation to evaluate

        :return: Evaluation score of the conversation in full
        :rtype: float
        """
        raise NotImplementedError
