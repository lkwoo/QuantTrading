import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import DatabaseManager as dbm
from matplotlib.ticker import MaxNLocator

class DrawChart():
    DBINFO = 'postgresql://postgres:asd123123@localhost:5432/stock'
    def __init__(self):
        self.db = dbm.DatabaseManager(self.DBINFO)

    def get_price_for_draw(self, code, to_df=False):
        query = f'''
            select code, market, name, date, stage, price
                , ema_5 , ema_12, ema_20, ema_26, ema_40
                , macd, macd_5_20, macd_5_40, macd_20_40
                , signal, signal_5_20, signal_5_40, signal_20_40
            from price_detail
            where code = '{code}'
            order by date
        '''
        if to_df:
            return pd.read_sql(query, self.db.get_conn())
        return self.db.fetch_all(query)
    
    def draw_graph_of_broken_line(self, code):
        df = self.get_price_for_draw(code, True)
        print(df['price'])
        print(df['ema_5'])
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['price'], linestyle='-', color='blue', label='price')
        plt.plot(df['date'], df['ema_5'], linestyle='-', color='green', label='ema5')
        plt.plot(df['date'], df['ema_20'], linestyle='-', color='orange', label='ema20')
        plt.plot(df['date'], df['ema_40'], linestyle='-', color='red', label='ema40')
        plt.title(f'Price Trend for Code: {code}, Market: {df["market"][0]}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(nbins=30))
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()
        plt.show()

# 조건을 만족하는지 확인하는 함수
def check_conditions(stock_data):
    # 1. ema5가 ema20, ema40을 아래에서 위로 크로스한지 5일 이내 확인
    crossed_above = (stock_data['ema5'] > stock_data['ema20']) & (stock_data['ema5'] > stock_data['ema40'])
    cross_dates = crossed_above[crossed_above].index
    if len(cross_dates) == 0 or (stock_data.index[-1] - cross_dates[-1]).days > 5:
        return False
    
    # 2. macd가 우상향인지 확인
    macd_slope = stock_data['macd'].diff()
    if macd_slope.iloc[-1] <= 0:
        return False

    return True

if __name__ == '__main__':
    tmp = DrawChart()
    tmp.draw_graph_of_broken_line('005930.KS')