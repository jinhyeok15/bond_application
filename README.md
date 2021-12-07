# Bond interest rate model prediction service

## Site
<http://jinpfo.site:8000>

## Documentation
<a href="doc/log.md">[Log]</a>   
<a href="doc/code.md">[Code description]</a>

## Service instruction

1. 
The service shows data about 5-maturity-yield 
which is labeled by credit rates that is evaluated by KIS(Korea Investors Service).
The data was crawled up to five years ago based on the current date and stored in the database. 
To visualize the data, the web server use python matplotlib and stores plot images 
to AWS S3 storage. The data is refreshed every 24 hours, server stores current data and removes oldest data.

2.
Starting from five years ago, we show the return model derived based on the algorithm as the actual model 
and obtain numerical data on how much the model deviates from the actual model.
The user inquires the most optimized model and actual yield graph on the home screen.
When the Next button is pressed below, the graph is updated, and the graph of the new model and the actual yield graph appear.
If the model shows a greater similarity to the actual yield data than the existing model, the Next button is deactivated and the Optimize button is activated.
When the Optimize button is pressed, a new model replaces the existing model.
The return model reflected on the home screen can be inquired.

3. 
The service will update feature which is to create profile with login.
The person who finds optimal model, he/she records on dashboard.

## 기획안
[Oven](https://ovenapp.io/project/o8vtYBpYjX62sAiaNdtnWeLpGQoTB89X#k9II6)

1. 채권의 수익률을 DB로부터 가져와서 그래프로 시각화 (시각화 모듈은 matplotlib, 추후 chart.js활용하기)
2. volatility, e(dr/dt), 평균 수익률, 분기별 데이터와 같은 수치 나타내기
3. stochastic interest rate model을 보여주고, 해당 interest rate model과 실제 interest model을 비교했을 때 가장 정확도가 높은 
model을 optimize버튼을 통해 알고리즘에 반영시킬 수 있다. 만일 optimize 버튼이 활성화 되지 않을 경우, next버튼으로 
다음 가상 model을 보여줌.
4. 추후에 로그인을 통한 계정 프로필 생성 기능을 추가할 경우, 가장 적합한 model을 찾은 유저는 DashBoard에 기록된다.

## Data source
The application gets data from\
공공데이터포털: <https://www.data.go.kr/>\
KIS bond return data: <https://www.kisrating.co.kr/ratingsStatistics/statics_spread.do>
