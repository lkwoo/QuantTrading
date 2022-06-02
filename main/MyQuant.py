from email.policy import default
from time import get_clock_info
import FinanceDataReader as fdr 
# ValueError: No tables found 좀 고쳐라
# yfinance로 갈아 타야겠어 십발
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os

# 직전 종가
def get_close(code):
    today = datetime.today()
    end = today.strftime("%Y-%m-%d")
    start = today - relativedelta(5)
    start = start.strftime("%Y-%m-%d")
    
    df = fdr.DataReader(code, start, end)
    df = df[['Close']]
    return df.iloc[-1, 0]

# 종목코드, days일 이동평균
def get_moving_average(code, days):    
    today = datetime.today()
    end = today.strftime("%Y-%m-%d")
    start = today - relativedelta(days= days*2)
    start = start.strftime("%Y-%m-%d")
    
    df = fdr.DataReader(code, start, end)
    df = df[['Close']]
    
    sum = 0
    for i in range(-days, 0):
        sum += df.iloc[i, 0]
    
    return int(sum / days)
    

# 종목코드, months개월 수익률
def get_yield(code, months):
    today = datetime.today()
    end = today.strftime("%Y-%m-%d")
    start = today - relativedelta(months=months)
    start = start.strftime("%Y-%m-%d")
    
    df = fdr.DataReader(code, start, end)
    df = df[['Close']]
    
    return (df.iloc[-1, 0] - df.iloc[0, 0]) / df.iloc[0, 0] * 100


# 종목코드
# code의 모멘텀 스코어 리턴
# Momentum Score = (최근1개월수익률×12)+(최근3개월수익률×4)+(최근6개월수익률×2)+(최근12개월수익률×1)
def get_momentum_score(code) :
    score = 0.0
    score += get_yield(code, 1) * 12
    score += get_yield(code, 3) * 4
    score += get_yield(code, 6) * 2
    score += get_yield(code, 12) * 1

    return score


class KHK_Strategy:
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
        # print(MS)
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
        


if __name__ == "__main__":
    # print(get_moving_average('005930', 200)) # get 삼성전자 200일 이동평균
    # print(get_yield('005930', 12)) # 삼성전자 1년 수익률
    # print(get_momentum_score('005930')) # 삼성전자 모멘텀 스코어
    khk = KHK_Strategy()
    # khk.print_asset()
    # khk.rebalance_VAA()
    df = fdr.DataReader('LQD', '2022-05-01', '2022-05-31')
    print(df)
    print(get_close('035720'))