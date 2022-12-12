from typing import List

from templates.actor import Actor
from templates.metrics.template_metric import BaseEvalMetric
from templates.utterance import BaseUtterance


class DummyMetric(BaseEvalMetric):
    """
    Example utterance/conversation evaluation metric
    """
    def score_utterance(self, utterance: BaseUtterance, context: List[BaseUtterance], **kwargs) -> float:
        # Dummy metric, awards greater turn-wise scores for sentences further in the conversation
        # Caps score at 1.0
        if len(context) == 0:
            return 0.1
        return 1.0 - 1 / len(context)

    def score_conversation(self, conversation: List[BaseUtterance], **kwargs) -> float:
        # Scores bot responses across entire conversation, returns average turn-wise score
        scores = []
        for i, utterance in enumerate(conversation):
            if utterance.actor == Actor.BOT:
                # only evaluate bot responses
                scores.append(self.score_utterance(utterance=utterance, context=conversation[:i]))

        return sum(scores) / len(scores)
