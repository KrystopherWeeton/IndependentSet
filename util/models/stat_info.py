import util.formulas as formulas


class StatInfo:
    def __init__(self, data: [float]):
        if len(data) == 1:
            self.mean = data[0]
            self.std_dev = None
        else:
            self.mean = formulas.mean(data)
            self.std_dev = formulas.std_dev(data)