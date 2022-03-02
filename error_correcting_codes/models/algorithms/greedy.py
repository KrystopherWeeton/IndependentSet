from email.message import Message
from typing import List, Union

from error_correcting_codes.models.algorithms.algorithm import Algorithm
from error_correcting_codes.models.codes.ldpc import LDPC
from error_correcting_codes.models.message_tracker import MessageTracker
from util.array import hamming_dist


class Greedy(Algorithm):

    def __init__(self, verbose=False, debug=False, step_hook = None):
        super().__init__(MessageTracker, verbose, debug)
        self._step_hook = step_hook


    def _clear(self):
        pass


    def _run(self, msg: MessageTracker):
        # Set up tracker for the algorithm
        num_parities: int = msg.get_num_parities()


        # Run algorithm
        last_index: int = -1
        while msg.get_num_parities_satisifed() < num_parities:
            to_swap: int = msg.get_best_swap_index()
            if to_swap == last_index:
                self.verbose_print(f"Terminating due to local optimum stopping condition.")
                break
            self.debug_print(f"Chose {to_swap} which will satisfy {msg.get_num_parities_satisfied_by_swap(to_swap)}")
            msg.swap_index(to_swap)
            self.verbose_print(f"Satisfied = {msg.get_num_parities_satisifed()} / {num_parities}")
            self.verbose_print(f"New Message = '{msg.get_message_string()}'")
            self.step_hook(msg.get_message(), msg.get_num_parities_satisifed())
            last_index = to_swap
        

        # Set final solution and return
        self._solution: MessageTracker = msg
