# Add import from parent directory possible
import sys
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from lib.DataOperations import *
from lib.ReportSignals import *

# Creates CCI object
def CreateCCI(high,low,close,n = 14):
    return CCI(high,low,close,n)


# CCI object which creates CCI data
class CCI:

        def __init__(self, high, low, close, n=14):
            self.n     = n
            self.factor = 0.015
            self.cci  = self.InitCCI(high, low, close)

            # Signals
            fromBottom,fromTop=FindIntersections(self.cci,100)
            self.buy  = fromBottom
            fromBottom,fromTop=FindIntersections(self.cci,-100)
            self.sell = fromTop

        # Set CCI indicator
        def InitCCI(self,high, low, close):
            ct = (high + low + close) / 3
            self.rollingMean = CreateMovingAverage(ct, self.n)
            self.rollingStd  = CreateMovingStd(ct, self.n)
            data = pd.Series((ct - self.rollingMean) / (self.factor * self.rollingStd), name = 'CCI_' + str(self.n))
            return data

        # Export indicator signals to report
        def ExportSignals(self, reportSignals):
            a=1


        # Plot method
        def Plot(self):
            # CCI
            plt.plot(self.cci.index, self.cci, label='CCI' + str(self.n), linewidth=1.0, color = '#000000')

            #OverBought
            overBought = CreateDataLine(self.cci.index, 100, 100)
            plt.plot(overBought.index, overBought, '--', label='Overbought', linewidth=1.0, color = '#940006')
            #OverSold
            overSold = CreateDataLine(self.cci.index, -100, -100)
            plt.plot(overSold.index, overSold, '--', label='Oversold', linewidth=1.0, color = '#169400')

            # Signals plottting
            if (self.buy is not None and self.buy.size):
                plt.plot(self.buy.index, self.buy, 'o', color = '#000000', ms=8)
                plt.plot(self.buy.index, self.buy, 'o', label='Horiz. Buy', color = '#00FF00')
            if (self.sell is not None and self.sell.size):
                plt.plot(self.sell.index, self.sell, 'o', color = '#000000', ms=8)
                plt.plot(self.sell.index, self.sell, 'o', label='Horiz. Sell', color = '#FF0000')

            # Limits of plot
            #plt.ylim(top=100,bottom=-100)

