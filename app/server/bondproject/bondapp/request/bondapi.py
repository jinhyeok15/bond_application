from json.decoder import JSONDecodeError
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import json
from datetime import datetime, timedelta


def get_json_item(page, _max):
    key = OPEN_API_KEY.encode()

    # 현재 시간이 만일 00시-16시이면 어제 시간을 가져옴
    now_date = datetime.now().strftime('%Y%m%d')
    if 0<=int(_get_time())<=16:
        now_date = _get_yst(now_date)
    
    queryParams = '?' + urlencode({
        quote_plus('serviceKey') : key,
        quote_plus('pageNo') : page,
        quote_plus('numOfRows') : _max,
        quote_plus('resultType') : 'json',
        quote_plus('basDt') : now_date
    })
    
    response = urlopen(url+queryParams)
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


def _get_yst(str_date):  # 문자열 날짜 ex) '20180921'
    dateformat = '%Y%m%d'
    dte = datetime.strptime(str_date, dateformat)
    return (dte-timedelta(days=1)).strftime(dateformat)


def _get_time():  # 현재 시간
    return datetime.now().strftime('%H')


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


url = 'http://apis.data.go.kr/1160100/service/GetBondIssuInfoService/getBondBasiInfo'
OPEN_API_KEY = 'YGMVpil/AHi/wBtNL1n90yhai6K4kIez7xRbCUDpiYWzd4cuhNahumycXmM/7jWmILuERvt9hTzE1YBo+DnDmg=='
