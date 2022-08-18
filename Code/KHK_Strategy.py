import MyQuant as mq
import pandas as pd
from email.policy import default

from pandas_datareader import data as pdr

class KHK:
    

    def __init__(self):
        self.vaa = self.get_trade_info('VAA')        
        self.laa = self.get_trade_info('LAA')        
        self.dual = self.get_trade_info('DUAL')    
        
    def print_asset(self):
        print(self.vaa)    
        print(self.laa)    
        print(self.dual)    

    def get_trade_info(self, stg):
        df = pd.read_excel('./code/data/trade_info.xlsx', converters={'DATE':str,'STRATEGY':str, default:int})
        
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
        MS = []
        MS.append(['SPY', mq.get_momentum_score('SPY')])
        MS.append(['EFA', mq.get_momentum_score('EFA')])
        MS.append(['EEM', mq.get_momentum_score('EEM')])
        MS.append(['AGG', mq.get_momentum_score('AGG')])
        
        MS.append(['LQD', mq.get_momentum_score('LQD')])
        MS.append(['IEF', mq.get_momentum_score('IEF')])
        MS.append(['SHY', mq.get_momentum_score('SHY')])
        print(MS)
        if MS[0][1] > 0 and MS[0][2] > 0 and MS[0][3] > 0 and MS[0][4] > 0:
            print("challenge")
        else:
            print('stable')

    def rebalance_LAA(self, US_UI): # US's Unemployment Index. Search on Google
        # 자산의 25%씩 IWD, GLD, IEF에 투자, 나머지 25%는 
        # if SHY's today close < MA200 and US_UI > MA365: SHY
        # else: QQQ
        pass

    def rebalance_DUAL(self):
        # if get_yield(SPY, 12) > get_yield(BIL, 12): max(SPY, EFA)
        # else: AGG
        pass
        

if __name__ == "__main__": # 활용 예시
    khk = KHK()
    khk.print_asset()
    khk.rebalance_VAA()
    
