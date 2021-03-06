from json.decoder import JSONDecodeError
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import json
from datetime import datetime, timedelta

from .manipulation import Calc
from . import reqconf
import pandas as pd


BOND_API_URL = 'http://apis.data.go.kr/1160100/service/GetBondIssuInfoService/getBondBasiInfo'
OPEN_API_KEY = reqconf.OPEN_API_KEY
COLUMN_NAMES = [
        'scrsItmsKcdNm',  # 유가증권종목종류코드명
        'bondIssuCurCd', # 채권발행통화코드
        'bondIsurNm', # 채권발행인명
        'bondIssuDt',  # 채권발행일자
        'bondExprDt',  # 채권만기일자
        'bondIssuAmt',  # 채권발행금액
        'bondIntTcdNm', # 채권이자유형코드명
        'bondSrfcInrt',  # 채권표면이율
        'intPayCyclCtt', # 이자지급주기내용
        'kisScrsItmsKcdNm', # 한국신용평가유가증권종목종류코드명
    ]
MAX_DATA_AMOUNT = 20000


class OverMaxDataAmount(Exception):  # 검색할 데이터 수 초과시 에러
    def __init__(self):
        super().__init__(f'검색할 데이터 수가 최대치를 넘었습니다. 최대: {MAX_DATA_AMOUNT}')


def get_json_item(page, _max):
    key = OPEN_API_KEY.encode()
    if _max>MAX_DATA_AMOUNT:
        raise OverMaxDataAmount

    # 현재 시간이 만일 00시-16시이면 어제 시간을 가져옴
    now_date = datetime.now().strftime('%Y%m%d')
    if 0<=int(datetime.now().strftime('%H'))<=16:
        now_date = (datetime.strptime(now_date, '%Y%m%d')-timedelta(days=1)).strftime('%Y%m%d')
    
    queryParams = '?' + urlencode({
        quote_plus('serviceKey') : key,
        quote_plus('pageNo') : page,
        quote_plus('numOfRows') : _max,
        quote_plus('resultType') : 'json',
        quote_plus('basDt') : now_date
    })
    
    response = urlopen(BOND_API_URL+queryParams)
    json_api = response.read().decode("utf-8")
    try:
        json_file = json.loads(json_api)
        return json_file['response']['body']['items']['item']
    except JSONDecodeError:
        print('SERVICE ERROR: http error')


def get_data(json_item, column):
    item_list = json_item
    use_data_list = []
    for item in item_list:
        use_data = dict()
        for name in column:
            use_data[name] = item[name]
        
        use_data_list.append(use_data)
    return use_data_list


class Change(Calc):
    def df(self):
        column = self.column
        # 데이터프레임 형식으로 보여주기
        dct_data = dict()
        for name in column:
            dct_data[name] = []
        for i in range(len(self.data)):
            for c_name in column:
                dct_data[c_name].append(self.data[i][c_name])
        return pd.DataFrame(dct_data)
