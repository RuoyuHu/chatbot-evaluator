from templates.actor import Actor
from templates.utterance import BaseUtterance

class ExampleUtterance(BaseUtterance):
    """
    Example utterance object
    """
    def __init__(self, actor: Actor, text: str) -> None:
        super().__init__()
        self.actor = actor
        self.text = text

    def __str__(self) -> str:
        return f"{str(self.actor)}: {self.text}"
