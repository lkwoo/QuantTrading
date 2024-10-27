import yfinance as yf
import FinanceDataReader as fdr
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from io import StringIO
from pprint import pprint
import time
import col_info
import concurrent.futures

class DatabaseConnection:
    def __init__(self, dbinfo):
        self.dbinfo = dbinfo
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.dbinfo)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

class MovingAverageTrade(DatabaseConnection):
    def __init__(self, dbinfo, markets):
        super().__init__(dbinfo)
        self.dbinfo = dbinfo
        self.markets = markets

    def fetch_all(self, query, cursor_factory=None):
        with self as conn:
            with conn.cursor(cursor_factory = cursor_factory) as cur:
                try:
                    cur.execute(query)
                    return cur.fetchall()
                except Exception as e:
                    print(f"[Error: fetch_all] {query}\n\n{e}")
                    return

    def fetch_one(self, query, cursor_factory=None):
        with self as conn:
            with conn.cursor(cursor_factory = cursor_factory) as cur:
                try:
                    cur.execute(query)
                    return cur.fetchone()
                except Exception as e:
                    print(f"[Error: fetch_one] {query}\n\n{e}")
                    return

    def execute_query(self, query):
        with self as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query)
                    conn.commit()
                    return cur.rowcount
                except Exception as e:
                    print(f"[Error: execute_query] {query}\n\n{e}")
                    return

    def copy_from_csv_buffer(self, buffer, table_name, sep, columns):
        buffer.seek(0)

        with self as conn:
            with conn.cursor() as cur:
                try:
                    cur.copy_from(file=buffer, table=table_name, columns=columns, sep=sep)
                    conn.commit()
                    return cur.rowcount
                except Exception as e:
                    print(f"[Error: copy_from_csv_buffer] {e}")
                    return

    def write_log(self, path, text):
        with open(path, 'a') as f:
            f.write(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] {text}")

    def get_stock_code_list_for_yfinance(self, market):
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
            code = stocks['Code']
            code = [x + '.KS' for x in code]
        elif market == 'KOSDAQ':
            code = stocks['Code']
            code = [x + '.KQ' for x in code]
        elif market == 'NASDAQ' or market == 'NYSE':
            code = stocks['Symbol'].tolist()
        else:
            code = None

        return code

    def get_latest_date(self, code, table):
        return self.fetch_one(f"select max(date) from {table} where code = '{code}'")[0]

    def get_earliest_date(self, code, table):
        return self.fetch_one(f"select min(date) from {table} where code = '{code}'")[0]

    def get_query_insert_stock_info(self, code, market, info):
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

    def get_inserted_list(self):
        '''
        현재 날짜로 적재된 데이터가 있는 종목의 리스트
        '''
        
        query = '''
        select code
        from(
            select code, max(update_time) as utime
            from stock_info
            group by code
        ) as tmp
        where utime::date = CURRENT_DATE
        '''
        res = self.fetch_all(query)
        codes = []
        for code in res:
            codes.append(code[0])
        return codes

    def get_filtered_stock_list(self, market, to_date):
        '''
        재무재표 상 사지 않는 것이 권장되는 종목을 제외하고 리스트를 가져온다. 
        '''
        query = f'''
            select code 
            from stock_info as s
            where 1=1
                and update_time::date >= '{to_date}'
                and (profitMargins > 0 or profitMargins is null)
                and market = '{market}'
            group by code
            '''
        res = self.fetch_all(query)
        codes = []
        for code in res:
            codes.append(code[0])
        return codes

    def update_stock_info(self, markets):
        '''
        Stock Info Update
        '''
        # 병렬로 함수 실행
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.insert_stock_info, market) for market in markets]

            for future in concurrent.futures.as_completed(futures):
                print(future.result())

    def insert_stock_info(self, market):
        '''
        market 별로 오늘 날짜로 적재된 데이터 없는 종목의 데이터 적재
        '''
        start_time = time.time()
        print(market)
      
        inserted = self.get_inserted_list()
        codes = self.get_stock_code_list_for_yfinance(market)
        for code in codes:
            if code in inserted:
                print(f'{code} is inserted')
                continue
            try:
                tk = yf.Ticker(code)
                query = self.get_query_insert_stock_info(code, market, tk.info)
                print(f'{code}: {self.execute_query(query)}')
            except:
                print(f"{code} insert fail")
                continue
            
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

    def insert_price(self, ticker ,market
                            ,start_date=(datetime.today() - relativedelta(days=365)).strftime("%Y-%m-%d")
                            , end_date=datetime.today().strftime("%Y-%m-%d")):
        '''
        종목별로 가격 데이터를 적재합니다.
        '''
        raw = ticker.history(
            interval='1d',
            # redundancy for calculate moving average
            start=(datetime.strptime(start_date, '%Y-%m-%d') - relativedelta(days=20)).strftime("%Y-%m-%d"),
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
            
        data = {'code': [], 'market': [], 'name': [], 'date': [], 'price':[]}
        madf = pd.DataFrame(data)

        for i, (index, row) in enumerate(raw.iterrows()):
            if i < closest_business_day_index:
                continue
            
            try:
                new_data = {'code':ticker.info['symbol'], 
                            'name':ticker.info['shortName'],
                            'market': market,
                            'date': str(index)[:10],
                            'price': row['Close']}
                madf = pd.concat([madf, pd.DataFrame([new_data])], ignore_index=True)
            except:
                return 0

        buffer = StringIO()
        madf.to_csv(buffer, index=False, header=False, sep='|') 

        row_count = self.copy_from_csv_buffer(buffer, 'price', '|', madf.columns.tolist())
        return row_count

    def init_price_detail(self, code, date):
        query = f'''
        INSERT INTO public.price_detail
        select code, market, name, date, 0, price, price, price, price, price, price, 0, 0, 0, 0, 0, 0, 0, 0
        from price
        where code = '{code}'
        and date = '{date}'
        limit 1
        '''
        return self.execute_query(query)

    def get_stage(self, ema5, ema20, ema40):
        if ema5 >= ema20 and ema20 >= ema40:
            return 1
        elif ema20 >= ema5 and ema5 >= ema40:
            return 2
        elif ema20 >= ema40 and ema40 >= ema5:
            return 3
        elif ema40 >= ema20 and ema20 >= ema5:
            return 4
        elif ema40 >= ema5 and ema5 >= ema20:
            return 5
        elif ema5 >= ema40 and ema40 >= ema20:
            return 6
        else:
            return 0

    def insert_price_detail(self, ticker, latest_date, end_date=datetime.today().strftime("%Y-%m-%d")):
        '''
        insert into db
        col: code, market, name, date, stage, price, ema_5, ema_12, ema_20, ema_26, ema_40, macd, macd_5_20, macd_5_40, macd_20_40,
            signal,signal_5_20,signal_5_40,signal_20_40
        EMA = (2 * today_price + (N-1) * yesterday_ema) / (N+1)
        MACD = EMA(short) - EMA(long)
        Signal = MACD's 9 day EMA
        '''
        data = {'code': [], 'market':[],'name': [], 'date': [], 'stage': [], 'price': [],
                'ema_5': [], 'ema_12': [], 'ema_20': [],'ema_26': [], 'ema_40': [],
                'macd': [], 'macd_5_20': [], 'macd_5_40': [], 'macd_20_40': [],
                'signal': [], 'signal_5_20': [], 'signal_5_40': [], 'signal_20_40': []}
        madf = pd.DataFrame(data)

        p = self.fetch_one(f"select * from price_detail where code = '{ticker.info['symbol']}' and date = '{latest_date}'", DictCursor)
        
        price_detail_before = {
            'code': p[0], 'market': p[1], 'name': p[2], 'date': p[3], 'stage': p[4], 'price': p[5],
            'ema_5': p[6], 'ema_12': p[7], 'ema_20': p[8],'ema_26': p[9], 'ema_40': p[10],
            'macd': p[11], 'macd_5_20': p[12], 'macd_5_40': p[13], 'macd_20_40': p[14],
            'signal': p[15], 'signal_5_20': p[16], 'signal_5_40': p[17], 'signal_20_40': p[18]
        }
        
        query = f'''
        select code, market, name, date, price
        from price
        where code = '{ticker.info['symbol']}'
        and date > '{latest_date}'
        order by date
        '''
        rows = self.fetch_all(query)
        
        for row in rows:
            market = row[1]
            date = row[3]   
            price = row[4]
            ema5 = (price_detail_before['ema_5'] * 4 + price * 2) / 6
            ema20 = (price_detail_before['ema_20'] * 19 + price * 2) / 21
            ema40 = (price_detail_before['ema_40'] * 39 + price * 2) / 41
            price_detail_base = {
                'code':ticker.info['symbol'], 
                'market': market,
                'name':ticker.info['shortName'],
                'date': date,
                'price': price,
                'stage': str(int(self.get_stage(ema5, ema20, ema40))),
            }
            price_detail_ema = {
                'ema_5': ema5,
                'ema_12': (price_detail_before['ema_12'] * 11 + price * 2) / 13,
                'ema_20': ema20,
                'ema_26': (price_detail_before['ema_26'] * 25 + price * 2) / 27,
                'ema_40': ema40
            }
            price_detail_macd = {
                'macd': price_detail_ema['ema_12'] - price_detail_ema['ema_26'],
                'macd_5_20': price_detail_ema['ema_5'] - price_detail_ema['ema_20'],
                'macd_5_40': price_detail_ema['ema_5'] - price_detail_ema['ema_40'],
                'macd_20_40': price_detail_ema['ema_20'] - price_detail_ema['ema_40']
            }
            price_detail_signal = {
                'signal': (price_detail_before['signal'] * 8 + price_detail_macd['macd'] * 2) / 10,
                'signal_5_20': (price_detail_before['signal_5_20'] * 8 + price_detail_macd['macd_5_20'] * 2) / 10,
                'signal_5_40': (price_detail_before['signal_5_40'] * 8 + price_detail_macd['macd_5_40'] * 2) / 10,
                'signal_20_40': (price_detail_before['signal_20_40'] * 8 + price_detail_macd['macd_20_40'] * 2) / 10
            }
            price_detail = {}
            price_detail.update(price_detail_base)
            price_detail.update(price_detail_ema)
            price_detail.update(price_detail_macd)
            price_detail.update(price_detail_signal)
            price_detail_before = price_detail
            madf = pd.concat([madf, pd.DataFrame([price_detail])], ignore_index=True)

        buffer = StringIO()
        madf.to_csv(buffer, index=False, header=False, sep='|') 
        
        row_count = self.copy_from_csv_buffer(buffer, 'price_detail', '|', madf.columns.tolist())
        return row_count
    
    def update_price_detail(self, market, to_date):
        '''
        Insert recently data into 'price_detail' table.
        This method must be executed after 'db_update_price' is executed
        '''
        print(f"[Insert Price Detail] {market}")
        code_list = self.get_filtered_stock_list(market, to_date)
        
        self.write_log(f'price_detail_log_{market}.txt', f"Try to insert {len(code_list)} codes\n")
        for code in code_list:
            try:
                print(f'{market} - {code}')
                ticker = yf.Ticker(code)

                latest_date = self.get_latest_date(code, 'price_detail')

                if latest_date == None:
                    # EMA is affected by start date. So need to set redundancy for calculate
                    latest_date =  self.get_earliest_date(code, 'price')
                    if latest_date == None:
                        self.write_log(f'error_{market}.txt', f"[db_update_price_detail] fail to get date: {code}\n")
                        continue
                    self.init_price_detail(code, latest_date)
                    
                ticker = yf.Ticker(code)
                row_count = self.insert_price_detail(ticker, latest_date)

                self.write_log(f'price_detail_log_{market}.txt', f"udpate price_detail: {code}, row: {row_count}\n")
            except Exception as e:
                self.write_log(f'error_{market}.txt', f'error in {code}. {e}\n')

    def update_price(self, market, to_date):
        '''
        insert recently data into 'price' table
        '''
        print(f"[Insert Price] {market}")
        code_list = self.get_filtered_stock_list(market, to_date)
        self.write_log(f'price_log_{market}.txt', f"Try to insert {len(code_list)} codes\n")
        for code in code_list:
            try:
                print(f'{market} - {code}')

                latest_date = self.get_latest_date(code, 'price')
                if latest_date == None:
                    latest_date =  (datetime.today() - relativedelta(days=600)).strftime("%Y-%m-%d")
                start_date = (datetime.strptime(latest_date, '%Y-%m-%d')+ relativedelta(days=1)).strftime("%Y-%m-%d")

                ticker = yf.Ticker(code)
                row_count = self.insert_price(ticker, market, start_date)

                self.write_log(f'price_log_{market}.txt', f"udpate price: {code}, row: {row_count}\n")
            except Exception as e:
                self.write_log(f'error_{market}.txt', f'error in {code}. {e}\n')

    def update_price_data(self, markets, to_date):
        '''
        insert new price data ? 이름 왜 이렇게 햇지
        '''
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.update_price, market, to_date) for market in markets]

            for future in concurrent.futures.as_completed(futures):
                print(future.result())

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.update_price_detail, market, to_date) for market in markets]

            for future in concurrent.futures.as_completed(futures):
                print(future.result())

if __name__ == '__main__':
    dbinfo = 'postgresql://postgres:asd123123@localhost:5432/stock'
    markets = ['KOSPI','KOSDAQ','NASDAQ','NYSE']  # 'KOSPI','KOSDAQ','NASDAQ','NYSE'
    #markets = ['KOSPI']

    mat = MovingAverageTrade(dbinfo, markets)
    
    # insert_stock_info
    mat.update_stock_info(markets)
        
    # update price
    mat.update_price_data(markets, '2024-10-13') 