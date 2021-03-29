import util.formulas as formulas

class StatInfo:
    def __init__(self, data: [float]):
        self.mean = formulas.mean(data)
        self.std_dev = formulas.std_dev(data)