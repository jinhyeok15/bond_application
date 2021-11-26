from datetime import datetime as dte


# 계산에 필요한 칼럼
essential_columns = [
        'bondIssuDt',  # 채권발행일자
        'bondExprDt',  # 채권만기일자
        'bondIntTcdNm', # 채권이자유형코드명
        'bondSrfcInrt',  # 채권표면이율
        'intPayCyclCtt', # 이자지급주기내용
    ]


class CannotCalculateError(Exception):  # 계산용 칼럼이 빠져있을 때 exception
    def __init__(self, idx):
        super().__init__('계산에 필요한 칼럼이 빠져있습니다. -> '+essential_columns[idx])


class BlankDataError(Exception):  # 데이터가 들어있지 않음
    def __init__(self):
        super().__init__('데이터가 존재하지 않습니다.')


class Calc:
    def __init__(self, data):
        self.data = data
        if not data:
            raise BlankDataError
        
        # 필요한 칼럼이 존재하는지 여부 확인. 없으면 raise error
        self.column = data[0]
        exst_col = [False for i in range(len(essential_columns))]
        for c in self.column:
            for i, ec in enumerate(essential_columns):
                if ec == c:
                    exst_col[i] = True
        for i, b in enumerate(exst_col):
            if not b: raise CannotCalculateError(i)

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


if __name__=='__main__':
    from bondapi import get_json_item, get_data, Change
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
    df = a.df()
    b = Calc(data)
    cycle = b.cycle_delta()
    print(cycle)
