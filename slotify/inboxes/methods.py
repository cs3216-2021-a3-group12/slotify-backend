
from .models import Message


def add_message(receiver, title, content):
    """
    Add a message to the receiver's inbox.
    """
    message = Message(receiver=receiver, title=title, content=content)
    message.save()


