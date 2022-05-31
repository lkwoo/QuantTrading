import FinanceDataReader as fdr



print(fdr.__version__)
# 삼성전자(005930) 전체 (1996-11-05 ~ 현재)
# df = fdr.DataReader('005930')
# print(df)

# Apple(AAPL), 2017-01-01 ~ Now
df = fdr.DataReader('AAPL', '2017')
print(df)

# Ford(F), 1980-01-01 ~ 2019-12-30 (40년 데이터)
#df = fdr.DataReader('F', '1980-01-01', '2019-12-30')

# AMAZON(AMZN), 2017 (1년)
#df = fdr.DataReader('AMZN', '2017-01-01', '2019-12-31')

# Samsung(005930), 2000-01-01 ~ 2019-12-31
#df = fdr.DataReader('068270', '2000-01-01', '2019-12-31')

# country code: ex) 000150: Doosan(KR), Yihua Healthcare(CN)
# df = fdr.DataReader('000150', '2018-01-01', '2019-10-30') # KRX
# df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='KRX') # KRX (위와 동일)
# df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='SZSE') # SZSE
# df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='심천') # SZSE

# # TSE (도쿄증권거래소)
# fdr.DataReader('7203', '2020-01-01', exchange='TSE') # 토요타 자동차(7203)
# fdr.DataReader('7203', '2020-01-01', exchange='TSE') # 소프트뱅크그룹(7203)

# # HOSE (호치민증권거래소)
# fdr.DataReader('VCB', '2020-01-01', exchange='HOSE') # 베트남 무역은행(VCB)
# fdr.DataReader('VIC', '2020-01-01', exchange='HOSE') # Vingroup (JSC)

# # AMEX(아메리카증권거래소)
# fdr.DataReader('LNG', '2020-01-01', exchange='AMEX') # Cheniere Energy (LNG)
# fdr.DataReader('CBOE', '2020-01-01', exchange='AMEX') # Cboe Global Markets (CBOE)

# # KRX delisting stock data 상장폐지된 종목 가격 데이터 (상장일~상장폐지일)
# df = fdr.DataReader('036360', exchange='KRX-DELISTING')

# # KOSPI index, 2015 ~ Now
# ks11 = fdr.DataReader('KS11', '2015-01-01')

# # Indexes, 2015 ~ Now
# dji = fdr.DataReader('DJI', '2015-01-01') # Dow Jones Industrial(DJI)
# sp = fdr.DataReader('US500', '2015-01-01') # S&P 500 지수 (NYSE)

# # FX 환율, 1995 ~ 현재
# usdkrw = fdr.DataReader('USD/KRW', '1995-01-01') # 달러 원화
# usdeur = fdr.DataReader('USD/EUR', '1995-01-01') # 달러 유로화
# usdcny = fdr.DataReader('USD/CNY', '1995-01-01') # 달러 위엔화

# # 상품 선물 가격 데이터
# df = fdr.DataReader('NG') # NG 천연가스 선물 (NYMEX)
# df = fdr.DataReader('ZG') # 금 선물 (ICE)
# df = fdr.DataReader('ZI') # 은 선물 (ICE)
# df = fdr.DataReader('HG') # 구리 선물 (COMEX)

# # Bitcoin KRW price (Bithumbs), 2016 ~ Now
# btc = fdr.DataReader('BTC/KRW', '2016-01-01')

# # 채권 수익률
# df = fdr.DataReader('KR1YT=RR') # 1년만기 한국국채 수익률
# df = fdr.DataReader('KR10YT=RR') # 10년만기 한국국채 수익률

# df = fdr.DataReader('US1MT=X') # 1개월 만기 미국국채 수익률
# df = fdr.DataReader('US10YT=X') # 10년 만기 미국국채 수익률

# # KRX stock symbol list
# stocks = fdr.StockListing('KRX') # 코스피, 코스닥, 코넥스 전체
# stocks = fdr.StockListing('KOSPI') # 코스피
# stocks = fdr.StockListing('KOSDAQ') # 코스닥
# stocks = fdr.StockListing('KONEX') # 코넥스

# # NYSE, NASDAQ, AMEX stock symbol list
# stocks = fdr.StockListing('NYSE')   # 뉴욕거래소
# stocks = fdr.StockListing('NASDAQ') # 나스닥
# stocks = fdr.StockListing('AMEX')   # 아멕스

# # S&P 500 symbol list
# sp500 = fdr.StockListing('S&P500')

# # 기타 주요 거래소 상장종목 리스트
# stocks = fdr.StockListing('SSE') # 상해 거래소
# stocks = fdr.StockListing('SZSE') # 신천 거래소
# stocks = fdr.StockListing('HKEX') # 홍콩거래소
# stocks = fdr.StockListing('TSE') # 도쿄 증권거래소
# stocks = fdr.StockListing('HOSE') # 호치민 증권거래소

# # KRX stock delisting symbol list 상장폐지 종목 전체 리스트
# krx_delisting = fdr.StockListing('KRX-DELISTING')

# # KRX stock delisting symbol list and names 관리종목 리스트
# krx_adm = fdr.StockListing('KRX-ADMINISTRATIVE') # 관리종목


# # FRED 데이터
# m2 = fdr.DataReader('M2', data_source='fred') #  M2통화량
# nq = fdr.DataReader('NASDAQCOM', data_source='fred') # NASDAQCOM 나스닥종합지수
# hou_nas = fdr.DataReader(['HSN1F', 'NASDAQCOM'], data_source='fred') # HSN1F 주택판매지수, NASDAQCOM 나스닥종합지수 

# # 캔들차트 그리기
# df = fdr.DataReader('005930', '2021-01-01', '2021-02-15')

# fdr.chart.plot(df)
# fdr.chart.plot(df, title='삼성전자(005930)')

# # 차트 설정
# config = {'title':'fdr.chart.config()를 사용하여 설정을 한번에 지정할 수 있습니다', 
#           'width': 600, 
#           'height': 300,
#           'volume': True,
# }

# fdr.chart.config(config=config)
# fdr.cha