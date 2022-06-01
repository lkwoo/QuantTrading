from email.policy import default
import FinanceDataReader as fdr
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os

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
        #self.laa = self.get_trade_info('LAA')        
        #self.dual = self.get_trade_info('DUAL')    
        print(self.vaa)    

    def get_trade_info(self, stg):
        df = pd.read_excel('./main/data/trade_info.xlsx', converters={'DATE':str,'STRATEGY':str, default:int})
        # IWM IWD 차이 확인하기. 강환국 책으로
        res = {}
        if stg == 'VAA':
            for j in range(1, len(df)+1):                
                if df.iloc[-j, 1] == 'VAA':
                    df_tmp = df.iloc[-j]
                    for i in range(2, len(df_tmp) - 1): 
                        if int(df_tmp.iloc[i]) > 0:            
                            res[df.columns[0]] = df_tmp.iloc[0]     
                            res[df.columns[i]] = df_tmp.iloc[i]
                            break        
            return res
        elif stg == 'LAA':
            for j in range(1, len(df)+1):                
                if df.iloc[-j, 1] == 'VAA':
                    df_tmp = df.iloc[-j]
                    for i in range(2, len(df_tmp) - 1): 
                        if int(df_tmp.iloc[i]) > 0:            
                            res[df.columns[0]] = df_tmp.iloc[0]     
                            res[df.columns[i]] = df_tmp.iloc[i]
                            break        
            return res


if __name__ == "__main__":
    # print(get_moving_average('005930', 200)) # get 삼성전자 200일 이동평균
    # print(get_yield('005930', 12)) # 삼성전자 1년 수익률
    # print(get_momentum_score('005930')) # 삼성전자 모멘텀 스코어
    khk = KHK_Strategy()
    khk.get_trade_info('VAA')