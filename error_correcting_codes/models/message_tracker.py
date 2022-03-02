from copy import copy, deepcopy
from typing import Dict, List

import numpy as np

from error_correcting_codes.models.codes.ldpc import LDPC
from util.misc import validate
from util.models.solution import Solution

"""
NOTE:
    `satisfied_change_list` is an indicator for the change in the number of satisfied constraints
    that would occur for each bit if it was swapped. This could be positive, negative, or 0.

    `satisfied_indicator` is an indicator maintained for whether each parity is satified
"""

OOB = Exception("Out of bounds access")

class MessageTracker(Solution):

    def __init__(self, code: LDPC, message: np.array):
        self.code: LDPC = code
        self.set_message(message)

    def swap_index(self, index: int):
        if index < 0 or index >= self._msg_len:
            raise OOB
        # Swap the message array
        self._message[index] = 1 - self._message[index]
        constraints: List[int] = self.code.get_constraints_for_index(index)

        # Update the satisfied indicator in list
        # Swapping this bit, swaps the satisfied for each constraints
        for c in constraints:
            self._satisfied_indicator[c] = 1 - self._satisfied_indicator[c]
            """
                Update satisfied change list with changes
                
                This part is a bit confusing. If we swap the same index again, surely we just
                undo the work we have just done (simple); however, we have also messed a bit with
                all the bits which are present in the constraints we just swapped. If we take
                constraint c from 1 -> 0, and constraint c has some other vertex u, then swapping
                u before now would have resulted in -1 to satisfied constraints, but now results in
                a +1 change, so the indicator for u needs to have 2 added. However, if we swap from 0
                to 1, we need to remove 2 from u's indicator in the list.

                NOTE: We implicitly handle reversing `index` itself because it is present in every
                constraint, so it's current value is #(0 -> 1's) - #(1 -> 0's), and following the
                above process we get precsiely the negation of this value.
            """
            for u in self.code.get_indices_in_constraint(c):
                if self._satisfied_indicator[c] == 1:    # 0 -> 1 case
                    self._satisfied_change_list[u] -= 2
                else:                                   # 1 -> 0 case
                    self._satisfied_change_list[u] += 2

    def set_message(self, message: np.array):
        self._message: np.array = message
        self._msg_len: int = len(self._message)
        # Verify structure
        validate(self._msg_len == self.code.msg_len, "Invalid message length provided.")
        self._initialize()

    
    def _initialize(self):
        """Initialize trackers for speedy operations"""
        # Calculate parities satisfied
        self._satisfied_indicator: np.array  = self.code.calculate_parities(self._message)
        # Calculate swap parity count list
        self._satisfied_change_list: np.array = np.array([0] * self._msg_len)
        for c in self.code.get_constraints():
            if self._satisfied_indicator[c] == 1:
                # If satisfied, swapping would remove a satisfied parity constraint
                for j in self.code.get_indices_in_constraint(c):
                    self._satisfied_change_list[j] -= 1
            else:
                # If not satified, swapping would add a satisfied parity constraint
                for j in self.code.get_indices_in_constraint(c):
                    self._satisfied_change_list[j] += 1

    def get_message(self) -> np.array:
        return copy(self._message)
    
    def get_message_string(self) -> str:
        return "".join([str(x) for x in self.get_message()])
    
    def msg_len(self) -> int:
        return len(self._message)

    def get_num_parities_satisfied_by_swap(self, index: int) -> int:
        if index < 0 or index >= self._msg_len:
            raise OOB
        return self._satisfied_change_list[index]

    def get_best_swap_index(self) -> int:
        # Go through the list of indices and get the best swap index
        # TODO: Change (possibly) to heap implementation to support speed maxes?
        # Only really affects basic algorithm's effectiveness.
        return np.argmax(self._satisfied_change_list)
    
    def get_num_parities_satisifed(self) -> int:
        # TODO: Change to lazily evaluation this
        return sum(self._satisfied_indicator)

    def get_num_parities(self) -> int:
        return self.code.num_parities

    def get_num_parities_swapped_for_all_indices(self) -> List[int]:
        return copy(self._satisfied_change_list)
