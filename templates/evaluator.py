from typing import List, Callable, Union, Dict, Any

from templates.metrics.template_metric import BaseEvalMetric
from templates.utterance import BaseUtterance
from templates.chatbot import BaseChatbot


class BaseEvaluator:
    """
    Template conversation evaluator class

    Must have the following attributes to be compatible with other components
    """

    # List of evaluation metrics to evaluae given utterances/documents/chatbots
    metrics: List[BaseEvalMetric] = None

    # Metric weights to produce a weighted sum of the metrics, can be either a
    # list of flaots or a function that gives a list of floats when called
    weighting: Union[List[float], Callable] = None

    # config object, for addtional information, must be present
    config: Dict[str, Any] = None

    def score_utterance(self, utterance: BaseUtterance, context: List[BaseUtterance], **kwargs) -> float:
        """
        Scoring function, scores a single utterance given the context

        :param BaseUtterance        utterance: Utterance to be evaluated
        :param List[BaseUtterance]  context: Context with which to evaluate the utterance
        """
        raise NotImplementedError

    def score_document(self, document: List[BaseUtterance], **kwargs) -> float:
        """
        Scoring function, scores a given document/list of utterances and produces an
        overall score for the conversation
        """
        raise NotImplementedError

    def score_chatbot(self, chatbot: BaseChatbot, condition: Callable, **kwargs) -> float:
        """
        Scoring function, scores a given chatbot's reponses until a given condition
        is met i.e. conversation is deemed to be over
        """
        raise NotImplementedError
