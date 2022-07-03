from pandas_datareader import data as pdr
import yfinance as yf
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


class My_Quant:
    def __init__(self):
        self.vaa = self.get_trade_info('VAA')        
        self.laa = self.get_trade_info('LAA')        
        self.dual = self.get_trade_info('DUAL')    
        
    def print_asset(self):
        print(self.vaa)    
        print(self.laa)    
        print(self.dual)    

    def get_trade_info(self, stg):
        df = pd.read_excel('./main/data/trade_info.xlsx', converters={'DATE':str,'STRATEGY':str, default:int})
        
        res = {}        
        for j in range(1, len(df)+1):  # 최근 데이터부터 찾음   
            if df.iloc[-j, 1] == stg:  # 찾으려는 전략의 자산이라면
                df_tmp = df.iloc[-j]
                res[df.columns[0]] = df_tmp.iloc[0]
                res[df.columns[1]] = df_tmp.iloc[1]  
                for i in range(2, len(df_tmp) - 1): # 보유한 자산만 찾아서 
                    if int(df_tmp.iloc[i]) > 0:                           
                        res[df.columns[i]] = df_tmp.iloc[i]
                res[df.columns[-1]] = df_tmp.iloc[-1] # sum colmn
                break

        return res

    def rebalance_VAA(self):
        # if SPY, EFA, EEM, AGG의 MS > 0 : 가장 MS가 높은 ETF에 전부 투자
        # else 위 4개 ETF중 MS가 하나라도 0 이하면 LQD, IEF, SHY 중 가장 MS 높은거에 전부 투자
        MS = {}
        MS['SPY'] = get_momentum_score('SPY')
        MS['EFA'] = get_momentum_score('EFA')
        MS['EEM'] = get_momentum_score('EEM')
        MS['AGG'] = get_momentum_score('AGG')
        MS['LQD'] = get_momentum_score('LQD')
        MS['IEF'] = get_momentum_score('IEF')
        MS['SHY'] = get_momentum_score('SHY')
        print(MS)
        if MS['SPY'] > 0 and MS['EFA'] > 0 and MS['EEM'] > 0 and MS['AGG'] > 0:
            pass
        else:
            pass

    def rebalance_LAA(self, US_UI): # US's Unemployment Index
        # 자산의 25%씩 IWD, GLD, IEF에 투자, 나머지 25%는 
        # if SHY's today close < MA200 and US_UI > MA365: SHY
        # else: QQQ
        pass

    def rebalance_DUAL(self):
        # if get_yield(SPY, 12) > get_yield(BIL, 12): max(SPY, EFA)
        # else: AGG
        pass
        


if __name__ == "__main__": # 활용 예시
    print(get_moving_average("005930.ks", "5d"))
    print(get_yield("005930.ks", "6m"))
    print(get_momentum_score("005930.ks"))