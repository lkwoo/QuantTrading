# QuantTrading : Rule based asset allocation trading.  
- 주식매매 의사결정에 필요한 정보를 제공하는 프로그램을 만들어 보자.

### Directory  
```
- References: 참고 자료
- Code: python code for Quant
- Data: Data for Quant
```

### Usage
```
- 
```

### 용어 설명
```
- PER (Price Earning Ratio, 주가수익비율) : 낮을수록 저평가 되었다고 여겨진다. PER = 주가 / 주당순이익. 주당순이익 = 당기순이익 / 주식수. 
- PBR ()
- ROE
```
-------------------------------------------------------------------------------------
# Quant Strategy
## 강환국 전략
- 3개 전략에 자산의 1/3씩 분산 투자

### Information
- VAA
    - Momentum Score = (최근1개월수익률×12)+(최근3개월수익률×4)+(최근6개월수익률×2)+(최근12개월수익률×1)
- LAA
    - SPY의 200일 이동평균
    - 미국실업률
- Original Dual Momentum
    - SPY, EFA, BIL의 최근 12개월 수익률

### Function
- get_moving_average('code', 'days') # 종목코드, 일수
    - return code의 days일 이동평균
- get_yield('code', 'start', 'end') # 종목코드, 시작날짜, 끝날짜
    - return code의 start부터 end까지의 수익률
- get_momentum_score('code') # 종목코드
    - return code의 모멘텀 스코어

### VAA
- 레벨 : 고급
- 기대 CAGR : 15%
- 포함 자산 : 7개의 ETF
    - 공격형 자산 : SPY, EFA, EEM, AGG
    - 안전자산 : LQD, IEF, SHY
- 매수 전략 
    - 매월 말 공격형자산, 안전자산의 모멘텀 스코어 계산
    - 모멘텀스코어 = (최근1개월수익률×12)+(최근3개월수익률×4)+(최근6개월수익률×2)+(최근12개월수익률×1)     
    - 공격형자산 4개 모두 모멘텀스코어가 0 이상일 경우 포트폴리오 전체를 가장 모멘텀스코어가 높은 공격형 자산에 투자
    - 공격형자산 4개중 하나라도 모멘텀스코어가 0 이하일 경우 포트폴리오 전체를 가장 모멘텀스코어가 높은 안전자산에 투자
- 매도 전략
    - 월 1회 리밸런싱
- 근 50년간 투자했다면? 
    - CAGR : 17.7%
    - MDD : -16.1%
### LAA
- 레벨 : 중급
- 기대 CAGR : 10%
- 포함 자산
    - 고정자산 : IWD, GLD, IEF
    - 타이밍자산 : QQQ, SHY
- 매수 전략
    - 자산의 각 25%를 IWD, GLD, IEF에 투자
    - 나머지 25%는 QQQ 또는 SHY에 투자
        - 미국 S&P 500 지수가격이 200일 이동평균보다 낮고 미국 실업률이 12개월 이동평균보다 높은 경우 미국 단기 국채에 투자
        - 그렇지 않을 경우 나스닥에 투자 
- 매도 전략
    - 고정자산 연 1회 리밸런싱, 타이밍자산 월 1회 리밸런싱
- 근 50년간 투자했다면? 
    - CAGR : 10.9%
    - MDD : -15.2%

### Original Dual Momentum
- 레벨 : 초급
- 기대 CAGR : 10-15%
- 포함 자산
    - SPY, EFA, AGG
- 매수 전략 
    - 매월 말 SPY, EFA, BIL의 최근 12개월 수익률을 계산
    - SPY의 수익률이 BIL보다 높으면 SPY 또는  EFA 중 최근 12개월 수익률이 더 높은 ETF에 투자
    - SPY의 수익률이 BIL보다 낮으면 AGG에 투자
- 매도 전략
    - 월 1회 리밸런싱
- 근 50년간 투자했다면? 
    - CAGR : 15.1%
    - MDD : -19.6%
