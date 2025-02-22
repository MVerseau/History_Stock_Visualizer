import pandas_ta as pta
import inspect
from datetime import datetime, date
import pandas as pd


# Класс Индикатор "собирает" функции по расчёту каждого индикатора в отдельности
class Indicator:
    _instances = []

    def __init__(self, tech_indicators, data):
        self._instances.append(self)
        self.data = data
        self._indicators = self._verify_indr(tech_indicators)

    def _verify_indr(self, tech_indicators):
        for indr in tech_indicators:
            indr = indr.lower().replace(' ', '_')
            if indr in [fun[0] for fun in inspect.getmembers(Indicator, predicate=inspect.isfunction)]:
                func_name = getattr(self, indr)
                if not hasattr(self, 'indicators'):
                    self.indicators = dict()
                res = func_name(self.data)
                if type(res) in (pta.DataFrame, pta.Series):
                    self.indicators.setdefault(indr.lower(), res)
            else:
                indr = [input(
                    f'Индекса "{indr.upper()}" нет. Возможно, Вы допустили опечатку. Введите корректное название или нажмите "Ввод", чтобы пропустить: ')]
                if len(indr) > 0:
                    self._verify_indr(indr)

    '''
    При последующей постепенной реализации других индикаторов они автоматически будут появлятся в списке доступных индикаторов.
    def ao(self, data) -> pta.Series:
        ao = pta.ao(close=data['Close'])
        if not type(ao) == pta.Series:
            self._non_valid_results('AO')
        return ao
    '''

    def macd(self, data) -> pta.DataFrame:
        macd = pta.macd(close=data['Close'])
        if not type(macd) == pta.DataFrame:
            self._non_valid_results('MACD')
        return macd

    def rsi(self, data) -> pta.Series:
        rsi = pta.rsi(close=data['Close'])  # Оставила период по умолчанию (14 дней)
        if not type(rsi) == pta.Series:
            self._non_valid_results('RSI')
        return rsi

    def standard_deviation(self, data) -> pd.Series:
        standart_deviation = pta.stdev(data['Close'])
        if not type(standart_deviation) == pd.Series:
            self._non_valid_results('Standard Deviation of Close Price')
        return standart_deviation

    def _non_valid_results(self, indicator):
        print(f'Для рассчёта {indicator} недостаточно данных. {indicator} не будет рассчитан.')
        return


def export_data_to_csv(data, period, ticker):
    if not period['start'] is None:
        period['period'] = '_'.join(
            [datetime.strftime(datetime.date(d), '%d%m%Y') for d in period.values() if isinstance(d, datetime)])
    filename = f'{ticker}_{period['period']}_stock_price_{date.today()}.csv'.replace('-', '_')
    with open(filename, 'w', encoding='utf-8') as f:
        data.to_csv(f, sep=';')
    print(f"Данные сохранены в {filename}")


def calculate_and_display_average_price(data):
    print(f'Среднее значение цены закрытия за период: {data['Close'].mean():.6f}')


def notify_if_strong_fluctuations(data, fluctuation: float):
    result = data['Close'].agg(['min', 'max']).pct_change()
    if result.iloc[-1] * 100 > fluctuation:
        print(f"\033[91mВНИМАНИЕ: Высокая волатильность ({result.iloc[-1] * 100:.4f}% за период)!!! \033[00m")
