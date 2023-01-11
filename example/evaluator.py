import numpy as np

from typing import List, Callable

from example.metrics.dummy import DummyMetric
from example.utterance import ExampleUtterance

from templates.metrics import BaseEvalMetric
from templates.evaluator import BaseEvaluator
from templates.chatbot import BaseChatbot
from templates.actor import Actor


def _example_weighting_func(metrics: List[BaseEvalMetric]) -> List[float]:
    """
    Example weighting function

    :param List[BaseEvalMetric]   metrics: Metrics to generate weighting for
    """
    return np.ones(len(metrics)) / len(metrics)


class ExampleEvaluator(BaseEvaluator):
    """
    Example evaluator using the BaseEvaluator template
    """
    def __init__(self, config) -> None:
        super().__init__()

        # Exmple uses two DummyMetrics
        self.metrics = [
            DummyMetric(),
            DummyMetric()
        ]

        # Weighted average weighting
        self.weighting = lambda: _example_weighting_func(metrics=self.metrics)

        self.config = config

    def score_utterance(self, utterance: ExampleUtterance, context: List[ExampleUtterance], **kwargs) -> float:
        scores = [metric.score_utterance(utterance, context, **kwargs) for metric in self.metrics]
        scores = np.array(scores)

        weights = self.weighting
        if callable(self.weighting):
            weights = self.weighting()
        return weights @ scores

    def score_document(self, document: List[ExampleUtterance], **kwargs) -> float:
        scores = [metric.score_conversation(conversation=document, **kwargs) for metric in self.metrics]
        scores = np.array(scores)

        weights = self.weighting
        if callable(self.weighting):
            weights = self.weighting()
        return weights @ scores

    def score_chatbot(self, chatbot: BaseChatbot, condition: Callable, **kwargs) -> float:
        context = []
        # While conversation end condition not satisfied, continue to generate responses
        # from the chatbot
        while not condition(context, **kwargs):
            user_response = input(">")
            context.append(ExampleUtterance(actor=Actor.USER, text=user_response))
            if condition(context, **kwargs):
                break
            bot_response = chatbot.respond(context=context, actor=Actor.BOT)
            print(bot_response)
            context.append(bot_response)

            # Compute turn-level score
            turn_score = self.score_utterance(utterance=bot_response, context=context, **kwargs)

            print(f"Score for this turn is {turn_score}")

        print("Conversation Ended")
        # Compute document/conversation-level score
        conv_score = self.score_document(document=context)
        print(f"Total Conversation score is {conv_score}")
