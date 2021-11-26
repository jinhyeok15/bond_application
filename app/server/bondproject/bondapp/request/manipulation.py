import pandas as pd


# 계산에 필요한 칼럼
essential_columns = [
        'bondIssuDt',  # 채권발행일자
        'bondExprDt',  # 채권만기일자
        'bondIssuAmt',  # 채권발행금액
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
        l_col = data[0]
        exst_col = [False for i in range(len(essential_columns))]
        for c in l_col:
            for i, ec in enumerate(essential_columns):
                if ec == c:
                    exst_col[i] = True
        for i, b in enumerate(exst_col):
            if not b: raise CannotCalculateError(i)

        # 데이터프레임 형식으로 보여주기
        dct_data = dict()
        for name in l_col:
            dct_data[name] = []
        for i in range(len(data)):
            for c_name in l_col:
                dct_data[c_name].append(data[i][c_name])
        print(pd.DataFrame(dct_data))


if __name__=='__main__':
    from bondapi import get_json_item, get_data
    item = get_json_item(1, 5)
    false_columns = [
        'scrsItmsKcdNm',  # 유가증권종목종류코드명
        'bondIssuCurCd', # 채권발행통화코드
        'bondIsurNm', # 채권발행인명
        'bondIssuDt',  # 채권발행일자
    ]
    
    data = get_data(item, essential_columns)
    blank_data = []
    a = Calc(data)
    a
