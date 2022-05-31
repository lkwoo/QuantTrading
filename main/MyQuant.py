import FinanceDataReader as fdr
from datetime import datetime, timedelta

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
    
    return (sum / days)
    

# 종목코드, 시작날짜, 끝날짜
# code의 start부터 end까지의 수익률 리턴
def get_yield(code, start, end):
    pass


# 종목코드
# code의 모멘텀 스코어 리턴
def get_momentum_score(code) :
    pass


if __name__ == "__main__":
    print(get_moving_average('005930', 200)) # get 삼성전자 200일 이동평균
    
    