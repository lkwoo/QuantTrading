import pykrx as pkx  # https://github.com/sharebook-kr/pykrx
from pykrx import stock
from pykrx import bond

import FinanceDataReader as fdr  # https://github.com/financedata-org/FinanceDataReader

from pandas_datareader import data as pdr
import yfinance as yf  # https://github.com/ranaroussi/yfinance
yf.pdr_override()

from datetime import datetime
from dateutil.relativedelta import relativedelta
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
def get_yield(code, period):  #p: "2y", "3m", "10d"
    end = get_today()
    start = get_date_before(period)
    
    df = pdr.get_data_yahoo(code, start, end)
    df = df[['Close']]
    
    return (df.iloc[-1, 0] - df.iloc[0, 0]) / df.iloc[0, 0] * 100


# 종목코드
# code의 모멘텀 스코어 리턴
# Momentum Score = (최근1개월수익률×12)+(최근3개월수익률×4)+(최근6개월수익률×2)+(최근12개월수익률×1)
def get_momentum_score(code) :
    score = 0.0
    score += get_yield(code, "1m") * 12
    score += get_yield(code, "3m") * 4
    score += get_yield(code, "6m") * 2
    score += get_yield(code, "12m") * 1

    return score

def get_low_cap(market):
    pass

if __name__ == "__main__": # 활용 예시
    # print(get_moving_average("005930.ks", "5d"))
    # print(get_yield("005930.ks", "6m"))
    # print(get_momentum_score("005930.ks"))
    
    #update_data('005930.ks')
    # df = fdr.StockListing('KRX')
    
    tickers = stock.get_market_ticker_list(market="KOSPI") # KOSDAQ
    print(tickers)
    for ticker in tickers:
        code = stock.get_market_ticker_name(ticker)
        print(code)
    
    # print(pdr.get_data_yahoo('005930.ks', '2022-05-11'))