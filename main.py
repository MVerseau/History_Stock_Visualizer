import textwrap
import types

import data_download as dd
import data_plotting as dplt
# import test as dplt
from datetime import date
import data_analysis as da

def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")

    # Getting a ticket
    ticker, period, fluctuation, tech_indicators, export = dd.gather_input_data()

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Calculate and display average closing price per period
    da.calculate_and_display_average_price(stock_data)

    # Detecting and alerting high fluctuation being more than number of per cent set by the user (10 % by default) price change
    da.notify_if_strong_fluctuations(stock_data, fluctuation)

    # Calculating indicators
    if len(tech_indicators) != 0:
        indcs = da.Indicator(tech_indicators, stock_data)

    # Export data to .csv file.
    if export.lower() in 'lд':
        if len(da.Indicator._instances) != 0:
            stock_data = stock_data.join([v for v in indcs.indicators.values()], how='inner')
        da.export_data_to_csv(stock_data, period, ticker)

    # Plot the data
    if len(da.Indicator._instances) != 0:
        stock_data = (stock_data, indcs.indicators)
    else:
        stock_data = (stock_data,)
    dplt.create_and_save_plot(stock_data, ticker, period)


if __name__ == "__main__":
    main()
