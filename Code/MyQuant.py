import pykrx as pkx  # https://github.com/sharebook-kr/pykrx
from pykrx import stock
from pykrx import bond
# import FinanceDataReader as fdr  # https://github.com/financedata-org/FinanceDataReader
from pandas_datareader import data as pdr
import yfinance as yf  # https://github.com/ranaroussi/yfinance
yf.pdr_override()

from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import pandas as pd

# return 오늘 날짜, format("%Y-%m-%d")
def get_today(): 
    return datetime.today().strftime("%Y-%m-%d")

# return p기간 이전 날짜, format("%Y-%m-%d")
def get_date_before(p): #p: "2y", "3m", "10d"
    if p[-1] == "y":
        return (datetime.today() - relativedelta(years = int(p[:-1]))).strftime("%Y-%m-%d")
    elif p[-1] == "m":
        return (datetime.today() - relativedelta(months = int(p[:-1]))).strftime("%Y-%m-%d")
    elif p[-1] == "d":
        return (datetime.today() - relativedelta(days = int(p[:-1]))).strftime("%Y-%m-%d")

# return start부터 end까지 종가 테이블
def get_close(code, start, end):   # ex) get_close('005930.ks', s, e)
    close = pdr.get_data_yahoo(code, start, end)
    return close['Close']

# return period 기간 이동평균
def get_moving_average(code, period):  #p: "2y", "3m", "10d"
    end = get_today()
    start = get_date_before(period)
    
    df = pdr.get_data_yahoo(code, start, end)
    print(df)
    return df['Close'].mean()
    

# return period 기간 수익률
def get_yield(ticker, period):  #p: "2y", "3m", "10d"
    end = get_today()
    start = get_date_before(period)
    
    file_name = 'Data/' + ticker + '.csv'
    df = pd.read_csv(file_name)
    for index, row in df.iterrows():
        print(row['Date'], row['Close'])
    # print(df)
    
    return


# 종목코드
# code의 모멘텀 스코어 리턴
# Momentum Score = (최근1개월수익률×12)+(최근3개월수익률×4)+(최근6개월수익률×2)+(최근12개월수익률×1)
def get_13612W_momentum_score(ticker) :        
    df = pd.read_csv('Data/' + ticker + '.csv').sort_values('Date', ascending=False)
    
    month = get_today()[5:7]    
    score = 0.0    
    cnt = 0
    price = []

    for index, row in df.iterrows():
        if cnt == 13:
            break
        if month != row['Date'][5:7]:
            cnt += 1
            month = row['Date'][5:7]
            price.append(row['Close'])
            # print(row['Date'], row['Close'])
        
    today_close = df.iloc[0]["Close"]
    peroids = [(1, 12), (3, 4), (6,2),(12,1)]
    for p, w in peroids:
        earn = (today_close - price[p]) / price[p] * w
        # print(p, today_close, price[p], earn)
        score += earn

    return score

def get_low_cap(market):
    pass

def get_baa_etf_list():
    return ['QQQ', 'VWO', 'VEA', 'BND', 'TIP', 'DBC', 'BIL', 'IEF', 'TLT', 'LQD', 'SPY']

def baa_update_data():
    flist = os.listdir('./update')
    if get_today() in flist:
        return 'already updated!'
        
    etf_list = get_baa_etf_list()
    for etf in etf_list:
        data = pdr.get_data_yahoo(etf, start='2021-01-01', end=get_today())        
        file_name = 'Data/'+ etf + '.csv'
        data.to_csv(file_name)

    file_name = './update/' + get_today()
    f = open(file_name, 'w')
    f.close()
    return 'update date: ' + get_today()

if __name__ == "__main__": # 활용 예시
    # print(get_moving_average("005930.ks", "5d"))
    # print(get_yield("005930.ks", "6m"))
    # print(get_momentum_score("005930.ks"))
    
    #update_data('005930.ks')
    # df = fdr.StockListing('KRX')
    '''
    tickers = stock.get_market_ticker_list(market="KOSPI") # KOSDAQ
    print(tickers)
    for ticker in tickers:
        code = stock.get_market_ticker_name(ticker)
        print(code)
    '''
    # print(pdr.get_data_yahoo('005930.ks', '2022-05-11'))
    baa_update_data()
    etfs = get_baa_etf_list()
    for etf in etfs:
        print(etf)
        print(get_13612W_momentum_score(etf))
