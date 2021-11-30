# Bond interest rate model prediction service

## Data source
The application gets data from\
공공데이터포털: <https://www.data.go.kr/>\
KIS bond return data: <https://www.kisrating.co.kr/ratingsStatistics/statics_spread.do>

## Service instruction
When the application built, daily bond return data is stored at database, and calculate volatility that reflects current return data.

## 기획안
[12.1 변경사항]
1. 채권의 수익률을 DB로부터 가져와서 그래프로 시각화 (시각화 모듈은 matplotlib, 추후 chart.js활용하기)\
2. stochastic interest rate model을 보여주고, 해당 interest rate model과 실제 interest model을 비교했을 때 가장 정확도가 높은 
model을 optimize버튼을 통해 알고리즘에 반영시킬 수 있다. 만일 optimize 버튼이 활성화 되지 않을 경우, next버튼으로 
다음 가상 model을 보여줌.\
3. 추후에 로그인을 통한 계정 프로필 생성 기능을 추가할 경우, 가장 적합한 model을 찾은 유저는 DashBoard에 기록된다.\
   
[Oven] (https://ovenapp.io/project/o8vtYBpYjX62sAiaNdtnWeLpGQoTB89X#k9II6)

## Documentation
<a href="doc/log.md">[Log]</a>   
<a href="doc/code.md">[Code description]</a>   
