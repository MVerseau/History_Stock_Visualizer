import yfinance as yf
from datetime import datetime, timedelta


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


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)

    data = stock.history(period=period['period'], start=period['start'], end=period['end'])
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data
