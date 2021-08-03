from typing import List

import matplotlib.pyplot as plt

from util.misc import validate


class CandlePlot:
    """
    Used to plot candlesticks. Implemented as a class so indidivudal candlesticsk can be
    added indidivudally before all are plotted

    Ex.
    candle: CandlePlot = CandlePlot()
    candle.add_candlestick([1, 2, 3], "small_numbers")
    candle.add_candlestick([4, 5, 6], "big_numbers")
    candle.plot()
    """
    def __init__(self, showmeans: bool = False):
        self.data: List[List[float]] = []
        self.labels: List[str] = []
        self.showmeans: bool = showmeans

    def add_candlestick(self, data: List[float], label: str):
        self.data.append(data)
        self.labels.append(label)
    
    def plot(self):
        validate(len(self.data) > 0, "Can't plot candlesticks with no data")
        plt.boxplot(self.data, labels=self.labels, showmeans=self.showmeans)
