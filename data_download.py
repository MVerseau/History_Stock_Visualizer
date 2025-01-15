import yfinance as yf

def set_period(period):
    if set(period).intersection({".",'/','-'}):
        get_period(period)
    return period

def get_period(period, count=0):
    
    start=datetime.strptime(period.replace('-','/').replace('.','/').strip('"'),'%d/%m/%Y')
    #start=datetime.strftime(start, '%Y-%m-%d')
    end=input('Введите дату окончания периода ("дд.мм.гггг"): ')
    end=datetime.strptime(end.replace('-','/').replace('.','/').strip('\"'),'%d/%m/%Y')
    if end>start: # TODO: Предусмотреть ошибку при многократном вводе некорретной даты.
        count+=1
        print("Дата окончания периода раньше даты начала периода.")
        get_period(period)
    period=dict(start=start, end=end) #TODO: Проверить, что примет в рассчет stock.history
    #end=datetime.strftime(end, '%Y-%m-%d') 
    return period

def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data
