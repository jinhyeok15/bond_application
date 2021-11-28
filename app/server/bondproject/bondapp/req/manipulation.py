from datetime import datetime as dte
from functools import wraps


# 계산에 필요한 칼럼
ESSENTIAL_COLUMN = [
        'scrsItmsKcdNm',  # 유가증권종목종류코드명
        'bondIssuDt',  # 채권발행일자
        'bondExprDt',  # 채권만기일자
        'bondIntTcdNm', # 채권이자유형코드명
        'bondSrfcInrt',  # 채권표면이율
        'intPayCyclCtt', # 이자지급주기내용
        'kisScrsItmsKcdNm', # 한국신용평가유가증권종목종류코드명
    ]

# 필터링 하기 위해 넣어야할 이름 code mapping
# 유가증권종목종류코드명별
SCRS_ITMS_COL_NAME = {
    '01': '국채',  # 국채
    '02': '지방채',  # 지방채
    '03': '금융채',  # 금융채
    '04': '일반회사채',  # 일반회사채
    '05': '특수채',  # 특수채
    '06': '유동화SPC채',  # 유동화SPC채
    '07': 'MBS',  # MBS
    '08': 'SLBS',  # SLBS
    '09': '지방공사채',  # 지방공사채
    '10': '유사집합투자기구채',  # 유사집합투자기구채
}

# 채권이자유형코드명별
INT_TCD_COL_NAME = {
    '01': '이표채',  # 이표채
    '02': '할인채',  # 할인채
    '03': '단리채',  # 단리채
    '04': '복리채',  # 복리채
}

# 이자지급주기별
INT_CYCL_COL_NAME = {
    '01': '12개월',
    '02': '6개월',
    '03': '3개월',
    '04': '4개월',
    '05': '2개월',
    '06': '1개월',
}


class CannotCalculateError(Exception):  # 계산용 칼럼이 빠져있을 때 exception
    def __init__(self, idx):
        super().__init__('계산에 필요한 칼럼이 빠져있습니다. -> '+ESSENTIAL_COLUMN[idx])


class BlankDataError(Exception):  # 데이터가 들어있지 않음
    def __init__(self):
        super().__init__('데이터가 존재하지 않습니다.')


# filter
class Filter:
    def __init__(self, data):
        self.data = data
        if not self.data:
            raise BlankDataError
        
        # 필요한 칼럼이 존재하는지 여부 확인. 없으면 raise error
        self.column = self.data[0]
        exst_col = [False for i in range(len(ESSENTIAL_COLUMN))]
        for c in self.column:
            for i, ec in enumerate(ESSENTIAL_COLUMN):
                if ec == c:
                    exst_col[i] = True
        for i, b in enumerate(exst_col):
            if not b: raise CannotCalculateError(i)

    # def show_valid_column(self, col_nm):
    #     return list(set(list(map(lambda d: d[col_nm], self.data))))
    
    def filter(func):
        @wraps(func)
        def wrapper(self, filtnm):
            li = []
            for d in self.data:
                if d[func()]==filtnm:
                    li.append(d)
            self.data = li
            return self.data
        return wrapper

    @filter
    def filt_bndnm():  # 채권 종목별 조회
        return 'scrsItmsKcdNm'

    @filter
    def filt_ipaynm():  # 이자 지급 종류별 조회
        return 'bondIntTcdNm'

    @filter
    def filt_cycle():  # 이자 지급 주기별 조회
        return 'intPayCyclCtt'


class Calc(Filter):
    # 채권의 발행일, 만기일을 통해 만기 계산
    def bond_maturity(self):
        l_matur = []
        for d in self.data:
            issu = d['bondIssuDt']
            expr = d['bondExprDt']
            date_format = "%Y%m%d"
            dt_issu = dte.strptime(issu, date_format)
            dt_expr = dte.strptime(expr, date_format)
            delta = (dt_expr-dt_issu).days/365
            if .4<=delta-int(delta)<=.6:  # 반개월 반영
                delta = int(delta)+.5
            else:
                delta = int(round(delta))
            l_matur.append(delta)
        return l_matur

    # 이자지급주기 델타 계산: 개월/12
    def cycle_delta(self):
        import re  # str.replace()가 작동 안됨. 대신 re모듈 사용
        l_cycle = []
        for d in self.data:
            str_paycycl = re.sub('개월', '', d['intPayCyclCtt'])
            l_cycle.append(int(str_paycycl)/12)
        return l_cycle    
