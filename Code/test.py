import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 샘플 데이터 프레임 생성
data = {'Value': [10, 20, 30, 40, 50]}
dates = pd.date_range(start='2024-01-01', periods=5, freq='D')
df = pd.DataFrame(data, index=dates)

# DataFrame을 한 줄씩 읽으며 인덱스, 행 데이터 및 행의 순서 출력
for idx, (index, row) in enumerate(df.iterrows()):
    print("행 번호:", idx)
    print("인덱스:", index)
    print("데이터:", row)
    print(df.iloc[2])

start_date='2023-05-19'
print(start_date)
print((datetime.strptime(start_date, '%Y-%m-%d') - relativedelta(days=7)).strftime("%Y-%m-%d"))
start_date= (datetime.strptime(start_date, '%Y-%m-%d') - relativedelta(days=1)).strftime("%Y-%m-%d")
print(start_date)