import yfinance as yf
from datetime import datetime, timedelta


# Check whether a propriate period started
def set_period(period):
    # if set(period).intersection({r".", r'/', r'-'}):
    for i in (r".", r'/', r'-'):
        if i in period:
            period = get_period(period)

    return period


def get_period(period, count=0):
    start = datetime.strptime(period.replace('-', '/').replace('.', '/').strip('"'), '%d/%m/%Y')
    if start >= datetime.today():
        if count <= 3:
            count += 1
            print('Период должен начинаться раньше сегодняшнего дня.')
            get_period(period)
        else:
            print('Вы трижды ввели неверную дату начала периода')
            period = '1mo'
            return period
    # start=datetime.strftime(start, '%Y-%m-%d')
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
    period = dict(start=start, end=end)  # TODO: Проверить, что примет в рассчет stock.history

    # end=datetime.strftime(end, '%Y-%m-%d')
    return dict(start=start, end=end)


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(start=period['start'], end=period['end'])
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data
