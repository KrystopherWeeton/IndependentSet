import unittest
from subprocess import CompletedProcess, run
from typing import List

from error_correcting_codes.models.ldpc import LDPC
from error_correcting_codes.models.message_tracker import MessageTracker


class TestMessageTracker(unittest.TestCase):

    def setUp(self) -> None:
        pass


    def _assert_success(self, response: CompletedProcess):
        assert response.returncode == 0, f"Response Code: {response.returncode}, stdout='{response.stdout}'"


    def test_construction(self) -> None:
        """ Test simple construction """
        msg: MessageTracker = MessageTracker(
            LDPC(msg_len=12, num_parities=6, edge_count=3), [0] * 12
        )

    def test_references(self) -> None:
        """ Test that all returned references are appropriately shallow """
        msg: MessageTracker = MessageTracker(
            LDPC(msg_len=12, num_parities=6, edge_count=3), [0] * 12
        )
        message: List[int] = msg.get_message()
        parity_swaps: List[int] = msg.get_num_parities_swapped_for_all_indices()
        message[0] = -100
        parity_swaps[0] = -100
        assert msg.get_message()[0] != -100, "Shallow reference to message detected"
        assert msg.get_num_parities_swapped_for_all_indices()[0]  != -100, "Shallow refernec to num paritied detected"

    def test_set_message(self) -> None:
        """ Simple test case for setting the message appropriately after construction """
        msg: MessageTracker = MessageTracker(
            LDPC(msg_len=12, num_parities=6, edge_count=3), [0] * 12
        )
        msg.set_message([1]*12)
        assert all([x == 1 for x in msg.get_message()]), "Did not appropriately set message"


    def test_swap_index(self) -> None:
        """ Test case to test some of the swap bit functionality for sanity checks. Not completely. """ 
        msg: MessageTracker = MessageTracker(
            LDPC(msg_len=12, num_parities=6, edge_count=3), [0] * 12
        )
        # Figure out what the swap result is for index 0 in the first case
        og_swaps: int = msg.get_num_parities_satisfied_by_swap(0)
        # Swap the first index
        msg.swap_index(0)
        new_swaps: int = msg.get_num_parities_satisfied_by_swap(0)
        assert og_swaps == - new_swaps, f"Swaps don't undo each other. og_swaps={og_swaps}, new_swaps={new_swaps}"


if __name__ == "__main__":
    unittest.main()
