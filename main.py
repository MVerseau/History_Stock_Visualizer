import textwrap
import types

import data_download as dd
import data_plotting as dplt
# import test as dplt
from datetime import date
import data_analysis as da
import inspect


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")
    print("Индикаторы финансового рынка включают (можно указать один или несколько): ")
    print(textwrap.fill(
        f'{', '.join([fun[0].upper() for fun in inspect.getmembers(da.Indicator, predicate=inspect.isfunction) if '_' not in fun[0]])}',
        150))
    print()

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    fluctuation = float(input('Введите процент изменения цены для определения высокой волатильности: '))
    tech_indicators = input(
        'Нужно ли посчитать какие-либо индикаторы (перечислите)? Если нет, то ничего не вводите. ')
    export = input('Нужно ли данные сохранить в файл? (д/н) ')

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
        # Converting str into a set and then into a tuple
        tech_indicators = tuple(set(tech_indicators.lower().replace(',', ' ').replace('  ', ' ').split(
            ' ')))
        # Creating an Indicator class instance to calculate the requested indicators
        indcs = da.Indicator(tech_indicators, stock_data)

    # Export data to .csv file.
    if export.lower() in 'lд':
        filename = f'{ticker}_{period}_stock_price_{date.today()}.csv'.replace('-', '_')
        if len(da.Indicator._instances) != 0:
            stock_data = stock_data.join([v for v in indcs.indicators.values()], how='inner')
        da.export_data_to_csv(stock_data, filename)

    # Plot the data
    if len(da.Indicator._instances) != 0:
        stock_data = (stock_data, indcs.indicators)
    else:
        stock_data = (stock_data,)
    dplt.create_and_save_plot(stock_data, ticker, period)


if __name__ == "__main__":
    main()
