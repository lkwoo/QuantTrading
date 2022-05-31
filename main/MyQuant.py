import FinanceDataReader as fdr
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# 종목코드, days일 이동평균
def get_moving_average(code, days):    
    today = datetime.today()
    end = today.strftime("%Y-%m-%d")
    start = today - timedelta(days= days*2)
    
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
def get_momentum_score(code) :
    pass


if __name__ == "__main__":
    # print(get_moving_average('005930', 200)) # get 삼성전자 200일 이동평균
    print(get_yield('005930', 12)) # 삼성전자 1년 수익률
    