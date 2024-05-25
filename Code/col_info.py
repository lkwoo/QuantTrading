info_columns_mapper = {
    # 정보 관련
    'market': '상장종류',  # nasdaq, nyse, amex
    'sector': '섹터',
    'industry': '산업군',
    'recommendationKey': '종합매수의견',
    
    # 매매 정보 관련
    'sharesOutstanding': '발행주식수',
    'averageVolume10days': '종목평균거래량(10일)',
    'averageVolume': '종목평균거래량',
    #'heldPercentInstitutions': '기관보유비율',
    #'shortRatio': '일일공매도비율',
    #'sharesPercentSharesOut': '발행주식대비공매도비율',
    #'shortPercentOfFloat': '유동주식중공매도비율',
    
    # 가격 관련
    'marketCap': '시가총액',  # 200B:mega // 10B~200B:large // 2B-10B:medium // 300M~2B:small // 50M~300M:micro // ~50M:nano
    'currentPrice': '현재가',
    'fiftyDayAverage': '50일평균가',
    'twoHundredDayAverage': '200일평균가',
    'fiftyTwoWeekHigh': '52주최고가',
    'fiftyTwoWeekLow': '52주최저가',
    #'SandP52WeekChange': 'S&P_52주변동성',
    #'52WeekChange': '52주변동성',
    'ytdReturn': '연초대비수익률',
    'fiveYearAverageReturn': '5년연평균수익률',  # 5년연평균수익률
    'beta': '베타값',  # 5년 데이터, 개별주식의 변동률을 의미. 1에 가까울수록 시장과 가깝고, 1을 넘어가면 시장 대비 고변동, 0으로 가까우면 시장 대비 저변동 주식을 의미함.
    
    # 현금 창출, 매출 관련 (ttm)
    'totalRevenue': '총매출액',
    'grossProfits': '매출총이익',  # 매출이익(매출액 - 매출원가)
    'revenuePerShare': '주당매출액',
    'ebitda': 'EBITDA',  # 감가상각 등의 부가비용을 차감하기 전의 금액, 영업 활동을 통한 현금 창출 능력. 유형자산의 가치까지 포함하는 지표
    'ebitdaMargins': 'EBITDA마진',  # 유형자산의 유지비용을 고려한 기업의 현금 창출 능력
    
    # 재무 상태 관련 (mrq)
    'debtToEquity': '부채자본비율',
    'operatingCashflow': '영업현금흐름',  # 영업현금흐름 : 영업이익 - 법인세 - 이자비용 + 감가상각비
    'freeCashflow': '잉여현금흐름',  # 기업의 본원적 영업활동을 위해 현금을 창출하고, 영업자산에 투자하고도 남은 현금
    'totalCashPerShare': '주당현금흐름',
    'currentRatio': '유동비율',  # 회사가 가지고 있는 단기 부채 상환 능력
    'quickRatio': '당좌비율',  # 회사가 가지고 있는 단기 부채 상환 능력
    
    
    # 경영 효율 관련
    'returnOnAssets': '자기자본이익률',  # mrq : 간단히 말해, 얼마를 투자해서 얼마를 벌었냐
    'returnOnEquity': '총자산순이익률',  # mrq : ROE와 비교하여 기업이 가지고 있는 부채의 비중을 볼 때
    'grossMargins': '매출총이익률',  # ttm : 매출이익(매출액 - 매출원가) / 매출액 : 매출이익률, Gross Profit Margin (GPM)
    'operatingMargins': '영업이익률',  # ttm : 매출총이익 - 판관비 - 감가상각비
    'profitMargins': '순이익률',  # ttm : Net Income(순이익) / Revenue(총수익) : 순이익률, Net Profit Margin (NPM)
    
    # 기업 자산 관련
    'totalCash': '총현금액',
    'totalDebt': '총부채액',
    
    # 기업 가치 관련
    'priceToBook': 'PBR',  # 기업이 가진 순 자산에 비해 주가가 얼마나 비싼지
    'enterpriseValue': '기업가치',  # 기업가치 : 시가총액 + (총차입금 - 현금성 자산)
    'enterpriseToRevenue': 'EV/R',  # 매출액대비 기업가치 비율
    'enterpriseToEbitda': 'EV/EBITDA',  # EBITDA대비 기업가치 비율 : PER과 의미적으로 비슷한 지표
    'forwardEps': '선행1년EPS',  # 주당순이익, 보통 5년동안의 EPS를 관찰해서 추이를 봄
    'trailingEps': '1년EPS',  # 주당순이익 = 당기순이익 / 유통주식수
    'priceToSalesTrailing12Months': '1년PSR',  # 주가매출액비율 (1년 기준)
    'forwardPE': '선행1년PER',  # 향후 1년동안 예상되는 PER
    'trailingPE': '1년PER',  # 현재 PER. 기업이 한 주당 벌어들이는 순이익에 비해, 실제 주가가 몇 배가 되는 지 나타내는 지표. 고평가 저평가에 사용
    
    # 배당 관련
    'dividendYield': '배당수익률',  # 현재 기준 배당 수익률
    'payoutRatio': '배당성향',  # 20 ~ 60% 사이가 일반적.
    'trailingAnnualDividendYield': '1년배당수익률',  # 지난 1년간 배당 수익률
    'dividendRate': '주당수익달러',
    'trailingAnnualDividendRate': '1년주당수익달러',
    
    # 성장성 관련
    'revenueGrowth': 'mrq매출액증가율',  # Most Recent Quater
    'earningsGrowth': 'mrq수익상승률',
    'earningsQuarterlyGrowth': 'yoy수익상승률',  # yoy : 지난해 동일 분기 대비 최근 분기의 수익 상승률
    'revenueQuarterlyGrowth': 'yoy매출상승률',  # yoy : 지난해 동일 분기 대비 최근 분기의 매출 상승률
    #'heldPercentInsiders': '직원보유비율',
}

financial_columns_mapper = {
    #'Research Development': 'R&D비용',
    #'Net Income': '순이익',
    #'Gross Profit': '매출총이익',
    #'Operating Income': '영업이익',
    #'Total Revenue': '총매출',
    #'Cost Of Revenue': '제품원가',
}

balance_sheet_columns_mapper = {
    #'Total Liab': '총부채',
    #'Total Stockholder Equity': '자기자본',
    #'Total Assets': '총자산',
}

col_type_mapper = {
    'market': 'text',
    'code': 'text',
	'shortName': 'text',
	'sector': 'text',
	'industry': 'text',
	'recommendationKey': 'text',
	'sharesOutstanding': 'numeric',
	'averageVolume10days': 'numeric',
	'averageVolume': 'numeric',
	'marketCap': 'numeric',
	'currentPrice': 'numeric',
	'fiftyDayAverage': 'numeric',
	'twoHundredDayAverage': 'numeric',
	'fiftyTwoWeekHigh': 'numeric',
	'fiftyTwoWeekLow': 'numeric',
	'ytdReturn': 'numeric',
	'fiveYearAverageReturn': 'text',
	'beta': 'numeric',
	'totalRevenue': 'numeric',
	'grossProfits': 'numeric',
	'revenuePerShare': 'numeric',
	'ebitda': 'numeric',
	'ebitdaMargins': 'numeric',
	'debtToEquity': 'numeric',
	'operatingCashflow': 'numeric',
	'freeCashflow': 'numeric',
	'totalCashPerShare': 'numeric',
	'currentRatio': 'numeric',
	'quickRatio': 'numeric',
	'returnOnAssets': 'numeric',
	'returnOnEquity': 'numeric',
	'grossMargins': 'numeric',
	'operatingMargins': 'numeric',
	'profitMargins': 'numeric',
	'totalCash': 'numeric',
	'totalDebt': 'numeric',
	'priceToBook': 'numeric',
	'enterpriseValue': 'numeric',
	'enterpriseToRevenue': 'numeric',
	'enterpriseToEbitda': 'numeric',
	'forwardEps': 'numeric',
	'trailingEps': 'numeric',
	'priceToSalesTrailing12Months': 'numeric',
	'forwardPE': 'numeric',
	'trailingPE': 'numeric',
	'dividendYield': 'numeric',
	'payoutRatio': 'numeric',
	'trailingAnnualDividendYield': 'numeric',
	'dividendRate': 'numeric',
	'trailingAnnualDividendRate': 'numeric',
	'revenueGrowth': 'numeric',
	'earningsGrowth': 'numeric',
	'earningsQuarterlyGrowth': 'numeric',
	'revenueQuarterlyGrowth': 'numeric'
}

if __name__ == "__main__":
    for key in info_columns_mapper.keys():
        print(f'{key} text,')