from bondapi import get_json_item, get_data, Change
from manipulation import essential_columns

item = get_json_item(30, 10)
false_columns = [
    'scrsItmsKcdNm',  # 유가증권종목종류코드명
    'bondIssuCurCd', # 채권발행통화코드
    'bondIsurNm', # 채권발행인명
    'bondIssuDt',  # 채권발행일자
]

data = get_data(item, essential_columns)
blank_data = []
a = Change(data)
print(f"length: {len(a.filt_cycle('6개월'))}")
print(a.df())

# BlankError, CannotCalculateError 잘 뜨는지 확인
# 필터 함수 test
