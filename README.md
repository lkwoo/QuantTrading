# QuantTrading : Rule based asset allocation trading.  
- 주식매매 의사결정에 필요한 정보를 제공하는 프로그램을 만들어 보자.
- 다양한 투자 전략을 비교하고, 원하는 전략을 수행하는데 도움을 주는 기능을 제공하자.

### Directory  
```
- Code: python code for Quant
- Data: Data for Quant
- References: 참고 자료
```

### Usage
```
- 
```

### 용어 설명
``` 
- SMA(12) = 12개월 단순 이동 평균. 각 월말의 가격을 기준으로 평균을 구한다.
- SMA(12)-momentum = (현재가격 / SMA(12)) - 1
- Breadth Momentum = 현재 가격이 SMA(12)보다 낮은 안전 자산 ETF 수 / 전체 ETF 수
- 13612W-momentum = (1개월 수익 * 12) + (3개월 수익 * 4)  + (6개월 수익 * 2) + 12개월 수익
```
-------------------------------------------------------------------------------------
# Quant Strategy

### BAA-G12 (Bold Asset Allocation. Balanced)
```
- 공격형자산: SPY, QQQ, IWM, VGK, EWJ, VWO, VNQ, DBC, GLD, TLT, HYG, LQD
- 안전자산: TIP, DBC, BIL, IEF, TLT, LQD, BND
- 카나리아자산: SPY, VWO, VEA, BND
- 월 1회 리밸런싱
  
1. 카나리아 자산 4개 중 하나라도 13612W-momentum이 음수라면 안전자산에, 모두 양수라면 공격형자산에 투자    
2. 공격형자산 12개 중 SMA(12)-momentum이 가장 높은 6개의 ETF에 동일 비중(약 16.7%)분산 투자
3. 안전자산 7개 중 SMA(12)-momentum이 가장 높은 3개의 ETF에 동일 비중(약 33%) 분산 투자. 단, BIL의 SMA(12)-momentum보다 낮은 ETF는 BIL로 대체해서 투자.
    - ex) 3개 중 하나의 ETF가 BIL의 SMA(12)-momentum 보다 낮다면, 나머지 2개와 BIL에 분산 투자.
```

### BAA-G4 (Aggressive)
```
- 공격형자산: QQQ, VWO(EFA), VEA(EEM), BND(AGG)
- 안전자산: TIP, DBC, BIL, IEF, TLT, LQD, BND
- 카나리아자산: SPY, VWO, VEA, BND
- BAA-G12와 공격형 자산 투자 방식만 다르다.
- 월 1회 리밸런싱
  
1. 카나리아 자산 4개 중 하나라도 13612W-momentum이 음수라면 안전자산에, 모두 양수라면 공격형자산에 투자    
2. 공격형자산 4개 중 SMA(12)-momentum이 가장 높은 1개의 공격형 자산에 올인
3. 안전자산 7개 중 SMA(12)-momentum이 가장 높은 3개의 ETF에 동일 비중(약 33%) 분산 투자. 단, BIL의 SMA(12)-momentum보다 낮은 ETF는 BIL로 대체해서 투자.
    - ex) 3개 중 하나의 ETF가 BIL의 SMA(12)-momentum 보다 낮다면, 나머지 2개와 BIL에 분산 투자.
```

### 소형주 전략
```
- 시가총액 하위 10% 종목 중 필터로 거른 기업 중에서 투자
- 필터: 중국기업, 분기 적자 기업, 연 적자 기업, 지주사, 금융사, 관리종목
- 
```

### 이동 평균선 투자법
```
- 3개의 MACD(Moving Average Convergence / Divergence) 사용
- MACD: EMA (단) - EMA (장)
- Signal: MACD의 EMA(9)  (9일 지수이동평균)
- EMA: Exponential Moving Average
    . [EMA 계산] EMA(N) = (2 * today_price + (N-1) * yesterday_ema) / (N+1)
- 3개의 MACD와 Signal
  1. MACD (상): EMA(5) - EMA(20), Signal: MACD(상)의 EMA(9)
  2. MACD (중): EMA(5) - EMA(40), Signal: MACD(중)의 EMA(9)
  3. MACD (하): EMA(20) - EMA(40), Signal: MACD(하)의 EMA(9)
- 매도:
- 매수:
```
