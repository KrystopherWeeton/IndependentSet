import unittest


class MyTestCase(unittest.TestCase):
    def __init__(self):
        pass

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
