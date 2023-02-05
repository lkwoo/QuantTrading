import pykrx as pkx  # https://github.com/sharebook-kr/pykrx
from pykrx import stock
from pykrx import bond
# import FinanceDataReader as fdr  # https://github.com/financedata-org/FinanceDataReader
from pandas_datareader import data as pdr
import yfinance as yf  # https://github.com/ranaroussi/yfinance
yf.pdr_override()
# import dart_fss as dart

from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import pandas as pd

# return 오늘 날짜, format("%Y-%m-%d")
def get_today(): 
    return datetime.today().strftime("%Y-%m-%d")

# return p기간 이전 날짜, format("%Y-%m-%d")
def get_date_before(date, p): #p: "2y", "3m", "10d"
    date = datetime.strptime(date, '%Y-%m-%d')
    if p[-1] == "y":
        return (date - relativedelta(years = int(p[:-1]))).strftime("%Y-%m-%d")
    elif p[-1] == "m":
        return (date - relativedelta(months = int(p[:-1]))).strftime("%Y-%m-%d")
    elif p[-1] == "d":
        return (date - relativedelta(days = int(p[:-1]))).strftime("%Y-%m-%d")

# return start부터 end까지 종가 테이블
def get_close(code, start, end):   # ex) get_close('005930.ks', s, e)
    close = pdr.get_data_yahoo(code, start, end)
    return close['Close']
    
# 종목코드
# code의 모멘텀 스코어 리턴
# Momentum Score = (최근1개월수익률×12)+(최근3개월수익률×4)+(최근6개월수익률×2)+(최근12개월수익률×1)
def get_13612W_momentum_score(ticker, date = get_today()) :        
    df = pd.read_csv('Data/' + ticker + '.csv').sort_values('Date', ascending=False)
        
    score = 0.0    
    flag = True
    cnt = 0
    price = []
    latest_close = 0
    peroids = [[0, 1, 12], [1, 3, 4], [2, 6, 2], [3, 12, 1]]  # index, month, weight

    for index, row in df.iterrows():        
        if flag and date >= row['Date']:
            latest_close = row['Close']
            flag = False
        if cnt == 4:
            break        
        if get_date_before(date, str(peroids[cnt][1]) +'m') >= row['Date']:
            cnt += 1            
            price.append(row['Close'])
            # print(row['Date'], row['Close'])        
    
    for i, p, w in peroids:
        earn = (latest_close - price[i]) / price[i] * w * 100
        # print(p, latest_close, price[i], earn)
        score += earn

    return score


def get_SMA12M(ticker, date = get_today()):
    df = pd.read_csv('Data/' + ticker + '.csv').sort_values('Date', ascending=False)
    
    flag = True
    cnt = 0
    price = []
    latest_close = 0
    
    date_b = []
    for i in range(1, 13):
        date_b.append(get_date_before(date, str(i) + 'm'))

    for index, row in df.iterrows():                
        # 직전 월부터 12개월의 종가
        if flag and date >= row['Date']:
            latest_close = row['Close']
            flag = False
        if cnt == 12:
            break        
        if date_b[cnt] >= row['Date']:
            cnt += 1            
            price.append(row['Close'])      
            # print(row['Date'], price[-1])      
        
    sum = 0.0
    for p in price:
        sum += p
    SMA12 = sum / 12
    # print(SMA12)
    
    return (latest_close / SMA12) - 1


def get_lowcap_stock(percentage):  # percentage: 0~100
    df = stock.get_market_cap_by_ticker("20221028")
    df = df.sort_values(by=['시가총액'], axis=0, ascending=True)
    num = int(len(df) * (percentage / 100))
    df = df[:num]    
    return df

'''
def get_lowcap_in_dart(percentage): # filter 거래정지 등
    api_key = "29ecae32523c4e6023eda1b7888e95c85e83c3e9"
    dart.set_api_key(api_key=api_key)
    CL = dart.corp.CorpList()

    df = get_lowcap_stock(percentage)
    lowcap = []

    index = df.index
    for i in index:        
        corp = CL.find_by_stock_code(str(i), include_delisting=False,include_trading_halt=False)
        if corp == None:
            continue        
        lowcap.append(i + ", " + corp.corp_name)
    
    return lowcap
'''
def get_baa_etf_list():
    return ['QQQ', 'VWO', 'VEA', 'BND', 'TIP', 'DBC', 'BIL', 'IEF', 'TLT', 'LQD', 'SPY', 'EFA', 'EEM', 'AGG']

def baa_update_data(force = False):
    flist = os.listdir('./update')
    if get_today() in flist and force == False:
        return 'already updated!'
        
    etf_list = get_baa_etf_list()
    for etf in etf_list:
        data = pdr.get_data_yahoo(etf, start='2021-01-01', end=get_today())        
        file_name = 'Data/'+ etf + '.csv'
        data.to_csv(file_name)
    
    flist = os.listdir('./update')
    for f in flist:        
        os.remove('./update/' + f)
    file_name = './update/' + get_today()
    f = open(file_name, 'w')
    f.close()
    return 'update date: ' + get_today()

if __name__ == "__main__": # 활용 예시
    #low10p = get_lowcap_stock(10) # 하위 10퍼센트. dart_fss에 없는건 안 나와
    #print(len(low10p))
    #print(low10p)

    #dt = get_lowcap_in_dart(10)
    #print(len(dt))
    #print(dt)

    ## stock = yf.Ticker('005930.ks')
    # stock = yf.Ticker('AAPL')
    # print(stock.info['profitMargins'])
    # print(get_SMA12M('QQQ', '2022-11-01'))
    baa_update_data()
    #print(get_13612W_momentum_score('QQQ'))

   