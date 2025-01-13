import matplotlib.pyplot as plt
import pandas as pd


class PlotIndicator:
    @staticmethod
    def rsi(indicator_data, ax2):

        if 'Date' not in indicator_data:
            if pd.api.types.is_datetime64_any_dtype(indicator_data.index):
                dates = indicator_data.index.to_numpy()
                ax2.plot(dates, indicator_data.values, label=indicator_data.name.upper())

            else:
                print("Информация о дате отсутствует или не имеет распознаваемого формата.")
                return
        else:
            if not pd.api.types.is_datetime64_any_dtype(indicator_data['Date']):
                indicator_data['Date'] = pd.to_datetime(indicator_data['Date'])
            ax2.plot(indicator_data['Date'], indicator_data.name,
                     label=indicator_data.name.upper())

        ax2.set(xlabel="Дата", ylabel="Значение")
        ax2.legend()

        return ax2

    @staticmethod
    def macd(indicator_data, ax2):

        if 'Date' not in indicator_data:
            if pd.api.types.is_datetime64_any_dtype(indicator_data.index):
                dates = indicator_data.index.to_numpy()
                ax2.plot(dates, indicator_data[indicator_data.iloc[:, 0].name].values,
                         label=indicator_data.iloc[:, 0].name.upper(), color='blue')
                ax2.plot(dates, indicator_data[indicator_data.iloc[:, 1].name].values,
                         label='Histogram', color='green')
                ax2.plot(dates, indicator_data[indicator_data.iloc[:, 2].name].values, label="Signal", color='red')

            else:
                print("Информация о дате отсутствует или не имеет распознаваемого формата.")
                return
        else:
            if not pd.api.types.is_datetime64_any_dtype(indicator_data['Date']):
                indicator_data['Date'] = pd.to_datetime(indicator_data['Date'])
            ax2.plot(indicator_data['Date'], indicator_data[indicator_data.iloc[0].name],
                     label=indicator_data.name.upper(),
                     color='blue')
            ax2.plot(indicator_data['Date'], indicator_data[indicator_data.iloc[1].name], label='Histogram',
                     color='green')

            ax2.plot(indicator_data['Date'], indicator_data[indicator_data.iloc[2].name],
                     label='Signal',
                     color='red')

        ax2.set(xlabel="Дата", ylabel="Значение")
        ax2.legend()

        return ax2


def create_and_save_plot(data, ticker, period, filename=None):
    if len(data) == 1:
        create_and_save_price(data[0], ticker, period, filename)
    else:
        for k, v in data[1].items():
            # ----------------------Historical Price Plot ---------------
            fig = plt.figure(figsize=(20, 6))
            gs = fig.add_gridspec(4, hspace=0)
            ax1 = plt.subplot(gs[0:3, :])
            ax2 = plt.subplot(gs[3, :])

            if 'Date' not in data[0]:
                if pd.api.types.is_datetime64_any_dtype(data[0].index):
                    dates = data[0].index.to_numpy()
                    ax1.plot(dates, data[0]['Close'].values, label='Close Price')
                    ax1.plot(dates, data[0]['Moving_Average'].values, label='Moving Average')
                else:
                    print("Информация о дате отсутствует или не имеет распознаваемого формата.")
                    return

            else:
                if not pd.api.types.is_datetime64_any_dtype(data[0]['Date']):
                    data[0]['Date'] = pd.to_datetime(data[0]['Date'])
                ax1.plot(data[0]['Date'], data[0]['Close'], label='Close Price')
                ax1.plot(data[0]['Date'], data[0]['Moving_Average'], label='Moving Average')

            ax1.set(ylabel="Цена")
            ax1.tick_params(bottom=False, labelbottom=False)
            ax1.legend()

            # Indicators to Plot
            func_name = getattr(PlotIndicator, k)
            ax2 = func_name(data[1][k], ax2)

            fig.suptitle(f"{ticker.upper()}")

            # Sticking the plots
            plt.tight_layout()
            # plt.show()

            filename = f"{ticker}_{period}_stock_price_{k}_chart.png"

            plt.savefig(filename)
            print(f"График сохранен как {filename}")


def create_and_save_price(data, ticker, period, filename=None):
    plt.figure(figsize=(20, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")
