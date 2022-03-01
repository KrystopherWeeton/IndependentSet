import unittest
from subprocess import CompletedProcess, run
from typing import List


class TestCase(unittest.TestCase):


    def _assert_success(self, response: CompletedProcess):
        assert response.returncode == 0, f"Response Code: {response.returncode}, stdout='{response.stdout}'"
