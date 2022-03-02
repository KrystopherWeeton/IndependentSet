
from typing import List

from error_correcting_codes.models.message_tracker import MessageTracker
from util.random import coin_flip


def flip_message(msg_tracker: MessageTracker, p: float) -> List[int]:
    for i in range(msg_tracker.msg_len()):
        if coin_flip(p):
            msg_tracker.swap_index(i)
