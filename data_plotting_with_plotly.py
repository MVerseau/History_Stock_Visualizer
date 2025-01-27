import plotly.express as px
import pandas as pd
from datetime import datetime, date

pd.options.plotting.backend = "plotly"


#

class PlotIndicator:
    @staticmethod
    def rsi(indicator_data):
        rsi = pd.DataFrame(indicator_data)

        return rsi

    @staticmethod
    def macd(indicator_data):
        macd = indicator_data[[i for i in indicator_data]]

        return macd

    @staticmethod
    def standard_deviation(indicator_data):
        standard_deviation = pd.DataFrame(indicator_data)

        return standard_deviation



def create_and_save_plot(data, ticker):
    create_and_save_price(data[0], ticker)

    if len(data) != 1:
        for k, v in data[1].items():

            # Indicators to Plot
            func_name = getattr(PlotIndicator, k)
            df = func_name(data[1][k])
            labels = dict(index='Date', value='Value', variables='Legend')
            fig = df.plot(labels=labels, title=ticker.upper())
            fig.show()


def create_and_save_price(data, ticker):
    df = data[['Close', 'Moving_Average']]
    labels = dict(index='Date', value='Value', variables='Legend')
    fig = df.plot(labels=labels, title=ticker.upper())
    fig.show()
