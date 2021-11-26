# Log

## 11.24
* bondapi.py (-):   
함수 분리. 활용성 올리기
* bondapi.py (+):   
칼럼명에 따른 해당 데이터 추출이 가능하게 코드 변경할 것.

## 11.25
* 데이터 가공 파일 생성
	- manipulation.Calc
* bondapp/item -> bondapp/request로 rename
* src -> server rename

## 11.26
> bondapi.Change 객체는 Calc객체를 상속 받고 내부에서 calc_all()함수를 이용하여 데이터 가공
* bondapi test case manipulation에서 test하도록 옮기기
* Change객체 생성 및 df() 정의 후 test
* README rename Portal -> Documentation
* Calc.bond_maturity() 추가
* Calc.cycle_delta() 추가
* essential_columns에 칼럼 추가 => 유가증권종목종류코드명, 한국신용평가유가증권종목종류코드명
* Filter 객체 추가
