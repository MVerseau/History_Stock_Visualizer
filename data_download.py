import yfinance as yf
from datetime import datetime, timedelta
import inspect
import data_analysis as da

def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)

    data = stock.history(period=period['period'], start=period['start'], end=period['end'])
    return data

def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


# Check whether a propriate period started and get propriate period
def set_period(period):
    for i in (r".", r'/', r'-'):
        if i in period['period']:
            period['start'], period['end'] = get_period(period)
            period['period'] = None
            break
        else:
            period['start'], period['end'] = None, None
    return period


def get_period(period, count=0):
    start = datetime.strptime(period['period'].replace('-', '/').replace('.', '/').strip('"'), '%d/%m/%Y')
    if start >= datetime.today():
        if count <= 3:
            count += 1
            print('Период должен начинаться раньше сегодняшнего дня.')
            get_period(period)
        else:
            print('Вы трижды ввели неверную дату начала периода')
            period = '1mo'
            return period

    count = 0
    end = input('Введите дату окончания периода ("дд.мм.гггг"): ')
    end = datetime.strptime(end.replace('-', '/').replace('.', '/').strip('\"'), '%d/%m/%Y') + timedelta(days=1)
    if end < start:
        if count <= 3:
            count += 1
            print("Дата окончания периода раньше даты начала периода.")
            get_period(period)
        else:
            print('Вы трижды ввели неверную дату окончания периода')
            period = '1mo'
            return period

    return start, end

#Gathering indicators
def tech_indicators_list() -> tuple:
    print("Индикаторы финансового рынка включают (можно указать один или несколько): ")

    # Выборка доступных индикаторов
    indicators_list = [fun[0].replace('_', ' ').upper() for fun in
                       inspect.getmembers(da.Indicator, predicate=inspect.isfunction) if not fun[0].startswith('_')]

    indicators_dict = dict(list(enumerate(indicators_list)))

    # Вывод индикаторов в консоль
    for k, v in indicators_dict.items():
        print(f'{k + 1}. {v};')

    # Запрос индикаторов
    tech_indicators_input = input(
        'Нужно ли посчитать какие-либо индикаторы (перечислите, указав порядковый номер)? Если нет, то ничего не вводите. ')

    # Обработка строки
    tech_indicators_input = tech_indicators_input.strip().replace(' ', ',').replace(',,', ',').split(',')

    # Компановка в список, отсечение повторов, передача в нужном формате
    tech_indicators = []
    for k in tech_indicators_input:
        tech_indicators.append(indicators_dict[int(k) - 1].lower())

    tech_indicators = tuple(set(tech_indicators))

    return tech_indicators




# Gathering input data
def gather_input_data():
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).",
        end='\n\n')
    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    print()
    # Getting a period
    print(
        "Общие периоды времени для данных включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.\n Но в можете выбрать свой период.",
        end='\n\n')
    period = {'period': input(
        "Введите период для данных (например, '1mo' для одного месяца или начальную дату периода в виде 'дд.мм.гггг'): ")}
    period = set_period(period)
    print()
    # Fluctuation per cent
    fluctuation = float(input('Введите процент изменения цены для определения высокой волатильности: '))
    print()


    # Getting indicators
    tech_indicators = tech_indicators_list()
    print()

    # Acking whether to save data into a file
    export = input('Нужно ли данные сохранить в файл? (д/н) ')

    print("------------LET'S START------------------")

    return ticker, period, fluctuation, tech_indicators, export
