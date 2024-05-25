import yfinance as yf
import FinanceDataReader as fdr
import psycopg2
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from io import StringIO
from pprint import pprint
import time
import col_info


def get_stock_ticker_list_for_yfinance(market):
    '''
    특정 시장에 상장된 종목 조회
    아래 4개의 시장만 다룰 것이다
    KOSPI : KOSPI 종목
    KOSDAQ : KOSDAQ 종목
    NASDAQ : 나스닥 종목
    NYSE : 뉴욕증권거래소 종목
    '''
    stocks = fdr.StockListing(market)
    
    if market == 'KOSPI':
        ticker = stocks['Code']
        ticker = [x + '.KS' for x in ticker]
    elif market == 'KOSDAQ':
        ticker = stocks['Code']
        ticker = [x + '.KQ' for x in ticker]
    elif market == 'NASDAQ' or market == 'NYSE':
        ticker = stocks['Symbol'].tolist()
    else:
        ticker = None

    return ticker

def db_update_price(dbinfo, code):
    '''
    insert recently data into 'price' table
    '''
    with open('log.txt', 'a') as f:
        f.write(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] udpate price: {code}")

    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()
    query = f"select max(date) from price where code = '{code}'"
    cur.execute(query)
    latest_date = cur.fetchone()[0]
    if latest_date == None:
        latest_date =  (datetime.today() - relativedelta(days=400)).strftime("%Y-%m-%d")
    start_date = (datetime.strptime(latest_date, '%Y-%m-%d')+ relativedelta(days=1)).strftime("%Y-%m-%d")

    ticker = yf.Ticker(code)
    row_count = insert_price(dbinfo, ticker, start_date)

    with open('log.txt', 'a') as f:
        # print(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] udpate moving average: {code}, row: {row_count}")
        f.write(f", row: {row_count}\n")

def insert_price(dbinfo, ticker 
                        ,start_date=(datetime.today() - relativedelta(days=365)).strftime("%Y-%m-%d")
                        , end_date=datetime.today().strftime("%Y-%m-%d")):
    '''
    종목별로 가격 데이터를 적재합니다.
    '''
    raw = ticker.history(
        interval='1d',
        # redundancy for calculate moving average
        start=(datetime.strptime(start_date, '%Y-%m-%d') - relativedelta(days=365)).strftime("%Y-%m-%d"),
        end=end_date,
        actions=True,
        auto_adjust=True)

    while True:
        try:
            closest_business_day_index = raw.index.get_loc(start_date)
            break
        except:
            start_date = (datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(days=1)).strftime("%Y-%m-%d")
            if start_date > datetime.today().strftime("%Y-%m-%d"):
                return 0
        
    data = {'code': [], 'name': [], 'date': [], 'price':[]}
    madf = pd.DataFrame(data)

    for i, (index, row) in enumerate(raw.iterrows()):
        if i < closest_business_day_index:
            continue
        
        try:
            new_data = {'code':ticker.info['symbol'], 
                        'name':ticker.info['shortName'],
                        'date': str(index)[:10],
                        'price': row['Close']}
            madf = pd.concat([madf, pd.DataFrame([new_data])], ignore_index=True)
        except:
            return 0

    buffer = StringIO()
    madf.to_csv(buffer, index=False, header=False, sep='|') 
    buffer.seek(0)

    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()
    try:
        cur.copy_from(file=buffer, table='price', columns=madf.columns.tolist(), sep='|')
    except Exception as e:
        print(e)
        madf.to_csv(f'error_{datetime.today().strftime("%Y-%m-%d")}.csv', index=False, header=True, sep='|')
        return
    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()
    return row_count

def get_yesterday_ema(dbinfo, code, today):
    # if 데이터가 없는 초기 적재 상황:
    #     적재 시작 1년 전 날짜부터 EMA를 계산하여 적재 시작일의 EMA 계산
    #     함수 재귀로 다시 실행
    # else:
    #     price 테이블에서 가격을 가져와 ema 계산
    pass

def db_update_price_detail(dbinfo, code):
    '''
    insert recently data into 'price_detail' table
    '''
    with open('log.txt', 'a') as f:
        f.write(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] udpate price_detail: {code}")

    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()

    query = f"select max(date) from price_detail where code = '{code}'"
    cur.execute(query)
    
    latest_date = cur.fetchone()[0]
    yesterday_ema = 0

    if latest_date == None:
        # EMA is affected by start date. So need to set redundancy for calculate
        latest_date =  (datetime.today() - relativedelta(days=400)).strftime("%Y-%m-%d")
        # yesterday_ema
    else:
        start_date = (datetime.strptime(latest_date, '%Y-%m-%d')+ relativedelta(days=1)).strftime("%Y-%m-%d")

    ticker = yf.Ticker(code)
    row_count = insert_price_detail(dbinfo, ticker, start_date)

    with open('log.txt', 'a') as f:
        # print(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] udpate moving average: {code}, row: {row_count}")
        f.write(f", row: {row_count}\n")
    

def insert_price_detail(dbinfo, ticker 
                        ,start_date=(datetime.today() - relativedelta(days=365)).strftime("%Y-%m-%d")
                        , end_date=datetime.today().strftime("%Y-%m-%d")):
    '''
    insert into db
    col: code, name, date, price, stage, ema5, ema12, ema20, ema26, ema40, macd, macd9
    ema = (2 * today_price + (N-1) * yesterday_ema) / (N+1)
    '''
    raw = ticker.history(
        interval='1d',
        # redundancy for calculate moving average
        start=(datetime.strptime(start_date, '%Y-%m-%d') - relativedelta(days=100)).strftime("%Y-%m-%d"),
        end=end_date,
        actions=True,
        auto_adjust=True)

    while True:
        try:
            closest_business_day_index = raw.index.get_loc(start_date)
            break
        except:
            start_date = (datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(days=1)).strftime("%Y-%m-%d")
            if start_date > datetime.today().strftime("%Y-%m-%d"):
                return 0
        
    data = {'code': [], 'name': [], 'date': [], 'price':[],'stage':[],
            'ema5':[],'ema12':[],'ema20':[],'ema26':[],'ema40':[],'macd':[],'macd9':[]}
    madf = pd.DataFrame(data)

    for i, (index, row) in enumerate(raw.iterrows()):
        if i < closest_business_day_index:
            continue
        
        try:
            new_data = {'code':ticker.info['symbol'], 
                        'name':ticker.info['shortName'],
                        'date': str(index)[:10],
                        'price': row['Close'],
                        'ma3': raw.iloc[i-2:i+1]['Close'].sum() / 3 if len(raw.iloc[i-2:i+1]['Close']) == 3 else 0,
                        'ma5': raw.iloc[i-4:i+1]['Close'].sum() / 5 if len(raw.iloc[i-4:i+1]['Close']) == 5 else 0,
                        'ma7': raw.iloc[i-6:i+1]['Close'].sum() / 7 if len(raw.iloc[i-6:i+1]['Close']) == 7 else 0,
                        'ma20': raw.iloc[i-19:i+1]['Close'].sum() / 20 if len(raw.iloc[i-19:i+1]['Close']) == 20 else 0,
                        'ma50': raw.iloc[i-49:i+1]['Close'].sum() / 50 if len(raw.iloc[i-49:i+1]['Close']) == 50 else 0,
                        'ma60': raw.iloc[i-59:i+1]['Close'].sum() / 60 if len(raw.iloc[i-59:i+1]['Close']) == 60 else 0,
                        'ma120': raw.iloc[i-119:i+1]['Close'].sum() / 120 if len(raw.iloc[i-119:i+1]['Close']) == 120 else 0,
                        'ma200': raw.iloc[i-199:i+1]['Close'].sum() / 200 if len(raw.iloc[i-199:i+1]['Close']) == 200 else 0}
            madf = pd.concat([madf, pd.DataFrame([new_data])], ignore_index=True)
        except:
            return 0

    buffer = StringIO()
    madf.to_csv(buffer, index=False, header=False, sep='|') 
    buffer.seek(0)

    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()
    try:
        cur.copy_from(file=buffer, table='moving_average', columns=madf.columns.tolist(), sep='|')
    except Exception as e:
        print(e)
        madf.to_csv(f'error_{datetime.today().strftime("%Y-%m-%d")}.csv', index=False, header=True, sep='|')
        return
    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()
    return row_count

def get_query_insert_stock_info(code, market, info):
    # col_info.py에서 명시한 칼럼대로 DB에 넣자
    info['market'] = market
    info['code'] = code
    
    keys_list = list(col_info.col_type_mapper.keys())
    value_list = []

    for key in keys_list:
        value = info.get(key, None)
        if value is not None:
            if col_info.col_type_mapper[key] == 'text':
                value = value.replace("'", "''")
                value_list.append(f"'{value}'")
            elif col_info.col_type_mapper[key] == 'numeric':
                value_list.append(value)
            else:
                value_list.append('null')
        else:
            value_list.append('null')
    value_list = [str(item) for item in value_list]
    query = "insert into public.stock_info\n"
    query += f"({','.join(keys_list)})\n"
    query += "VALUES("
    query += f"{','.join(value_list)}"
    query += ")"
    
    return query.replace("Infinity", "null")

def excute_query(dbinfo, query):
    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    row_count = cur.rowcount
    cur.close()
    conn.close()
    return row_count

def get_inserted_list(dbinfo):
    '''
    현재 날짜로 적재된 데이터가 있는 종목의 리스트
    '''
    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()
    query = '''
    select code
    from(
        select code, max(update_time) as utime
        from stock_info
        group by code
    ) as tmp
    where utime::date = CURRENT_DATE
    '''
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    conn.close()
    codes = []
    for code in res:
        codes.append(code[0])
    return codes

def get_filtered_stock_list(dbinfo):
    '''
    재무재표 상 사지 않는 것이 권장되는 종목을 제외하고 리스트를 가져온다. 
    '''
    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()
    query = '''
        select code 
        from stock_info as s
        where 1=1
            and update_time::date = CURRENT_DATE
            and ((trailingpe < 20 and trailingpe > 5) or trailingpe is null) -- per
            and ((returnonequity < 0.2 and returnonequity > 0) or returnonequity is null) -- roa
            and (debtToEquity < 60 or debttoequity is null) -- 부채자본비율
            and (profitMargins > 0 or profitMargins is null)
            and recommendationkey not in ('underperform', 'sell')
            and code in (select code
                        from (
                        	select code, max(date) as mdate
                        	from price
                        	where 1=1 
                        	--and date < '2024-04-19'
                        	group by code
                        ) as tmp
                        --where mdate < '2024-04-19'
                        )
        order by market
        '''
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    conn.close()
    codes = []
    for code in res:
        codes.append(code[0])
    return codes

def insert_stock_info(dbinfo, markets):
    '''
    market 별로 오늘 날짜로 적재된 데이터 없는 종목의 데이터를 가져온다.
    '''
    print(get_inserted_list(dbinfo))
    for market in markets:
        start_time = time.time()
        print(market)
        # db_update_moving_average(dbinfo, code)
        inserted = get_inserted_list(dbinfo)
        tickers = get_stock_ticker_list_for_yfinance(market)
        for ticker in tickers:
            if ticker in inserted:
                print(f'{ticker} is inserted')
                continue
            try:
                tk = yf.Ticker(ticker)
            except:
                print(f"{ticker} insert fail")
                continue
            query = get_query_insert_stock_info(ticker, market, tk.info)
            print(f'{ticker}: {excute_query(dbinfo, query)}')
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")



if __name__ == '__main__':
    dbinfo = 'postgresql://postgres:asd123123@localhost:5432/stock'
    markets = ['KOSPI','KOSDAQ','NASDAQ','NYSE']  # 'KOSPI','KOSDAQ','NASDAQ','NYSE'

    # update price
    #'''
    #code_list = get_inserted_list(dbinfo)
    #print(len(code_list))
    code_list = get_filtered_stock_list(dbinfo)
    print(len(code_list))
    for code in code_list:
        print(code)
        db_update_price(dbinfo, code)
    #'''
    # insert_stock_info
    #insert_stock_info(dbinfo, markets)
    