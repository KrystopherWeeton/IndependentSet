import subprocess
import unittest


class TestExperiment(unittest.TestCase):

    def setUp(self) -> None:
        pass


    def test_successive_augmentation(self) -> None:
        """
        Test successive augmentation compiles and runs
        """
        response: subprocess.CompletedProcess = subprocess.run(
            args="./exp.py ind-set sa -n 500 --num-trials 1 --transient",
            capture_output=True,
            shell=True,
        )
        assert response.returncode == 0, f"Response Code: {response.returncode}, stdout='{response.stdout}'"



if __name__ == "__main__":
    unittest.main()
