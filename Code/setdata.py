import yfinance as yf
import FinanceDataReader as fdr
import psycopg2
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from io import StringIO

def get_stock_ticker_list_for_yfinance(market):
    '''
    특정 시장에 상장된 종목 조회
    밑의 4개의 시장만 다룰 것이다
    KOSPI : KOSPI 종목
    KOSDAQ : KOSDAQ 종목
    NASDAQ : 나스닥 종목
    NYSE : 뉴욕증권거래소 종목
    '''
    stocks = fdr.StockListing(market)
    print(stocks)
    
    if market == 'KOSPI':
        ticker = stocks['Code']
        ticker = [x + '.KS' for x in ticker]
    elif market == 'KOSDAQ':
        ticker = stocks['Code']
        ticker = [x + '.KQ' for x in ticker]
    elif market == 'NASDAQ' or market == 'NYSE':
        ticker = stocks['Symbol']
    else:
        ticker = None

    return ticker

def get_stock_price_info(code):
    '''
    '''

    pass

def insert_moving_average(dbinfo, ticker 
                        ,start_date=(datetime.today() - relativedelta(days=365)).strftime("%Y-%m-%d")
                        , end_date=datetime.today().strftime("%Y-%m-%d")):
    '''
    insert into db
    col: code, name, date, price, ma3, ma5, ma7, ma20, ma50, ma60, ma120, ma200
    '''
    raw = ticker.history(
        interval='1d',
        start=(datetime.strptime(start_date, '%Y-%m-%d') - relativedelta(days=365)).strftime("%Y-%m-%d"),
        end=end_date,
        actions=True,
        auto_adjust=True)
    
    print(raw)
    data = {'code': [], 'name': [], 'date': [], 'price':[],'ma3':[],'ma5':[],'ma7':[],'ma20':[],'ma50':[],'ma60':[],'ma120':[],'ma200':[]}
    madf = pd.DataFrame(data)

    while True:
        try:
            th = raw.index.get_loc(start_date)
            break
        except:
            start_date = (datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(days=1)).strftime("%Y-%m-%d")
            if start_date > datetime.today().strftime("%Y-%m-%d"):
                return
        
    for i, (index, row) in enumerate(raw.iterrows()):
        if i < th:
            continue
        
        new_data = {'code':ticker.info['symbol'], 
                    'name':ticker.info['shortName'],
                    'date': str(index)[:10],
                    'price': row['Close'],
                    'ma3': raw.iloc[i-2:i+1]['Close'].sum() / 3,
                    'ma5': raw.iloc[i-4:i+1]['Close'].sum() / 5,
                    'ma7': raw.iloc[i-6:i+1]['Close'].sum() / 7,
                    'ma20': raw.iloc[i-19:i+1]['Close'].sum() / 20,
                    'ma50': raw.iloc[i-49:i+1]['Close'].sum() / 50,
                    'ma60': raw.iloc[i-59:i+1]['Close'].sum() / 60,
                    'ma120': raw.iloc[i-119:i+1]['Close'].sum() / 120,
                    'ma200': raw.iloc[i-199:i+1]['Close'].sum() / 200}
        madf = pd.concat([madf, pd.DataFrame([new_data])], ignore_index=True)

    buffer = StringIO()
    madf.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    conn = psycopg2.connect(dbinfo)
    cur = conn.cursor()
    table_name = 'moving_average'
    columns = madf.columns.tolist()
    cur.copy_from(buffer, table_name, columns=columns, sep=',')
    conn.commit()
    row_count = cur.rowcount
    print("삽입된 행 수:", row_count)
    cur.close()
    conn.close()


if __name__ == '__main__':
    #res = get_stock_ticker_list_for_yfinance('KOSDAQ')
    #print(res)
    temp = ['000660.KS', 'AAPL']
    '''
    for tk in temp:
        ticker = yf.Ticker(tk)
        print(ticker.info)
        res = ticker.history(
            interval='1d',
            start='2024-01-20',
            end='2024-02-29',
            actions=True,
            auto_adjust=True)
        #print(res)
        #print(fdr.StockListing('KOSPI'))
    '''
    ticker = yf.Ticker('AAPL')
    print(ticker.info)
    dbinfo = 'postgresql://postgres:asd123123@localhost:5432/stock'
    insert_moving_average(dbinfo, ticker, '2021-01-01')