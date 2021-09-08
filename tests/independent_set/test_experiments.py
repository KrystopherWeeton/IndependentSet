import unittest
from subprocess import CompletedProcess, run


class TestExperiment(unittest.TestCase):

    def setUp(self) -> None:
        pass


    def _assert_success(self, response: CompletedProcess):
        assert response.returncode == 0, f"Response Code: {response.returncode}, stdout='{response.stdout}'"


    def test_successive_augmentation(self) -> None:
        """
        Test successive augmentation compiles and runs
        """
        response: CompletedProcess = run(
            args="./exp.py ind-set sa -n 100 --num-trials 1 --transient",
            capture_output=True,
            shell=True,
        )
        self._assert_success(response)


    def test_heuristic(self) -> None:
        """
        Test that heuristic experiment compiles and runs
        """
        response: CompletedProcess = run(
            args="./exp.py ind-set heuristic -n 100 --num-trials 1 --transient",
            capture_output=True,
            shell=True,
        )
        self._assert_success(response)

if __name__ == "__main__":
    unittest.main()
