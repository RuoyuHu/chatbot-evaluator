import torch
from typing import List, Dict, Any

from transformers import AutoModelForSequenceClassification, AutoTokenizer

from templates.metrics import BaseEvalMetric
from templates.actor import Actor

from example.utterance import ExampleUtterance


# Toggle to decide whether to use GPU in inference
USE_CUDA = True
CUDA = USE_CUDA and torch.cuda.is_available()
DEVICE = 'cuda' if CUDA else 'cpu'

# Configuration for tokenization
ENCODE_CONFIG = {
    "return_tensors": "pt",
    "max_length": 1024,  # Necessary due to maximum context length supported by DialogRPT
    "truncation": True
}

class DialogRPTMetric(BaseEvalMetric):
    def __init__(self, model_type) -> None:
        super().__init__()
        print(f"Initialising DialogRPTMetric")

        print(f"Loading DialogRPT Model")
        self.model = AutoModelForSequenceClassification.from_pretrained(model_type)
        if CUDA:
            self.model = self.model.to(DEVICE)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(model_type)

        print(f"Finished loading DialogRPTMetric")

    def score_utterance(self, utterance: ExampleUtterance, context: List[ExampleUtterance], **kwargs) -> float:
        # Tokenize input
        model_input = '\n'.join(list(map(str, context)))
        model_input = model_input + "<|endoftext|>" + str(utterance)
        model_input = self.tokenizer.encode(model_input, **ENCODE_CONFIG)
        model_input = model_input.to(DEVICE)

        result = self.model(model_input, return_dict=True)

        return torch.sigmoid(result.logits).squeeze().item()

    def score_conversation(self, conversation: List[ExampleUtterance], store: Dict[str, Any] = None, **kwargs) -> float:
        # Scores bot responses across entire conversation, returns average turn-wise score
        scores = []
        for i, utterance in enumerate(conversation):
            if utterance.actor == Actor.BOT:
                # only evaluate bot responses
                scores.append(self.score_utterance(utterance=utterance, context=conversation[:i]))

        # Enable return of scores per turn on top of document level score using store object
        if store is not None and "scores_per_turn" in store:
            store['scores_per_turn'] = scores

        return sum(scores) / len(scores)


