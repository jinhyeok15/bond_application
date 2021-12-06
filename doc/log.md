# Log

## 11.24
+ bondapi.py (-):   
함수 분리. 활용성 올리기
+ bondapi.py (+):   
칼럼명에 따른 해당 데이터 추출이 가능하게 코드 변경할 것.

## 11.25
+ 데이터 가공 파일 생성
	- manipulation.Calc
+ bondapp/item -> bondapp/request로 rename
+ src -> server rename

## 11.26
> bondapi.Change 객체는 Calc객체를 상속 받고 내부에서 calc_all()함수를 이용하여 데이터 가공
+ bondapi test case manipulation에서 test하도록 옮기기
+ Change객체 생성 및 df() 정의 후 test
+ README rename Portal -> Documentation
+ Calc.bond_maturity() 추가
+ Calc.cycle_delta() 추가
+ essential_columns에 칼럼 추가 => 유가증권종목종류코드명, 한국신용평가유가증권종목종류코드명
+ Filter 객체 추가
+ MAX_DATA_AMOUNT 설정 및 에러 생성

## 11.27
+ 각각의 필터링할 칼럼의 요소들을 추출해서 리스트로 확인 후, 해당 리스트들을 manipulation에 추가
+ test.py 추가
+ const한 변수명 전부 대문자로 변경
+ return.py get_date() -> get_date(soup)
+ fin => 채권 계산, 시각화 모듈 패키지
+ return.py -> kis.py rename

## 11.28
+ db설계 완료

## 11.29
+ Selenium으로 KIS 수익률 테이블 크롤링 후, 데이터베이스에 저장

## 12.1

## 12.3
> matplotlib로 시각화하기 (KIS 채권 수익률만)\
> runserver시 24시간 지나면 자동적으로 오래된 데이터 지우고, 최신 데이터 저장(수익률)
+ html static 파일 추가 경로 세팅 및 test용 css class 추가

## 12.4
+ home화면 structure 설계

## 12.5
+ home화면 content title 작업
+ 필터 박스 추가 및, plot container추가
+ static/js 추가, 필터 구현하기

## 12.6
+ 필터 완성
