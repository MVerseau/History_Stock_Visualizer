import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    print(f'Среднее значение цены закрытия за период: {data['Close'].mean():.6f}')


def notify_if_strong_fluctuations(data, fluctuation: float):
    result = data['Close'].agg(['min', 'max']).pct_change()
    if result.iloc[-1]*100 > fluctuation:
        print(f"\033[91mВНИМАНИЕ: Высокая волатильность ({result.iloc[-1]*100:.4f}% за период)!!! \033[00m")

