from templates.actor import Actor

class BaseUtterance:
    """
    Template utterance class

    Must have the following attributes to be compatible with other components
    """
    actor: Actor = None # Utterance speaker
    text: str = None    # Utterance content/body
