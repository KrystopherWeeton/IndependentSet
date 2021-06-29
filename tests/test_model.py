

"""
    Very simple test model class that is used to set up an extremely
    simple but sufficient testing suite.
"""
class TestModel:
    def __init__(self):
        raise Exception("Abstract")
    

    def run_tests(self) -> int:
        raise Exception("Abstract")

    
    def num_tests(self) -> int:
        raise Exception("Abstract")

    
    def identifier(self) -> str:
        raise Exception("Abstract")