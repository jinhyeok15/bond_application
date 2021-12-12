import boto3
from bondproject.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME, AWS_STORAGE_BUCKET_NAME
)

import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bondproject.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
from bondapp.models import BondYld

from matplotlib import pyplot as plt
import matplotlib.font_manager as fonm
import matplotlib as mat
mat.rcParams["font.family"] = 'batang'

import datetime
import os
from bondapp.req.kis import all_type_set, RATING_TYPE
from pykrx import stock


NOW = datetime.datetime.now()
STR_NOW = NOW.strftime('%Y%m%d')
STR_YST = (NOW-datetime.timedelta(days=1)).strftime('%Y%m%d')


def actPlot(type):
    data = BondYld.objects.filter(bond_type=type)
    str_date = data[0].date
    first = datetime.datetime.strptime(str_date, '%Y.%m.%d')
    str_date = data[len(data)-1].date
    last = datetime.datetime.strptime(str_date, '%Y.%m.%d')
    max_delta = int((last-first).days)
    x = []
    y = []
    for d in data:
        str_dte = d.date
        dte = datetime.datetime.strptime(str_dte, '%Y.%m.%d')
        delta = int((last-dte).days)
        x.append(max_delta-delta)
        y.append(float(d.five_year))
    plt.plot(x, y, label=f'{type}')

    x_date = []
    arr_days = [0, int(max_delta/4), int(max_delta*2/4), int(max_delta*3/4), max_delta]
    for nday in arr_days:
        nday=nday
        tme_delta = datetime.timedelta(days=nday)
        x_date.append((first+tme_delta).strftime('%Y.%m.%d'))
    plt.xticks(arr_days, x_date)
    return plt


S3_CLIENT = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME
                      )


def update_plt(type_arr):  # type_arr
    for i, typ in enumerate(type_arr):
        plt.clf()  # plt 초기화
        plot = actPlot(typ)
        plot = actPlot('국고채')  # 모델링한 plot으로 refactoring modelPlot(i)

        file_name = f'{STR_NOW}_{i}'
        file_path = f'media/{file_name}.png'
        plot.savefig(file_path)
        response= S3_CLIENT.upload_file(file_path, AWS_STORAGE_BUCKET_NAME, file_path)
        if os.path.exists(file_path):
            os.remove(file_path)

# 주의***: 추후에 db의 가장 마지막 칼럼의 날짜의 파일을 삭제하도록 변경할 것
def delete_plt(type_arr):
    for i in range(len(type_arr)):
        file_name = f'{STR_YST}_{i}' # STR_YST로 변경할 것 [12.10]
        file_path = f'media/{file_name}.png'
        response = S3_CLIENT.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_path)

# delete_plt(RATING_TYPE)
# update_plt(RATING_TYPE)
df = stock.get_index_ohlcv_by_date("20161129", "20211126", "1001")
# df['수익률'] = df['종가'] / df['종가'][0]
df = df['2021']
print(df.tail())
