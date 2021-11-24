# Bond interest rate model prediction service

## Data source
The application gets data from\
공공데이터포털: <https://www.data.go.kr/>\
KIS bond return data: <https://www.kisrating.co.kr/ratingsStatistics/statics_spread.do>

## Service instruction
When the application built, daily bond return data is stored at database, and calculate volatility that reflects current return data.

## 기획안
채권 데이터 중, 국채 데이터만 끌어오기에는 데이터 양이 너무 부족함. 20000여개의 데이터를 모두 사용해야 효율성을 높일 수 있을 듯.\
채권의 유가증권종목종류코드명(국고채, 특수채 등)과 이자지급방식별 분류(이표채, 복리채 등)를 활용하여, 모든 채권의 채권 가격을 계산하여 수익율 데이터를 반영하는 것이 나을 듯. KIS의 수익률 데이터는 AI 정답 데이터로 활용하고, 채권 API 데이터는 AI 학습용 데이터로 구분. 채권 API데이터에서 얻은 수익률들을 그래프로 시각화 하고, 가장 최신의 데이터로부터 1개월 뒤의 수익률을 예측할 것. 예측한 수익률은 1개월 뒤에 실제 수익률과 비교한 편차로 DB에 저장되며, 지속적으로 강화학습을 시켜 모델의 정확도를 높인다.

## Portal
<a href="doc/log.md">[Log]</a>   
<a href="doc/code.md">[Code description]</a>   
