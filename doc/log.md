# Log

## 11.24
* bondapi.py (-):   
함수 분리. 활용성 올리기
* bondapi.py (+):   
칼럼명에 따른 해당 데이터 추출이 가능하게 코드 변경할 것.

## 11.25
- 데이터 가공 파일 생성
	- manipulations.Calc
- bondapi.Change 객체는 Calc객체를 상속 받고 내부에서 calc_all()함수를 이용하여 데이터 가공
- bondapp/item -> bondapp/request로 rename
- src -> server rename
