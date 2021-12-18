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
import re
from bondapp.req.kis import all_type_set, RATING_TYPE
from bondapp.fin.figure import *
from pykrx import stock
import pandas as pd


NOW = datetime.datetime.now()
STR_NOW = NOW.strftime('%Y%m%d')
STR_YST = (NOW-datetime.timedelta(days=1)).strftime('%Y%m%d')


def _get_obj(bond_type):
    return BondYld.objects.filter(bond_type=bond_type)


def actPlot(type):
    data = _get_obj(type)
    str_date = data[0].date
    first = datetime.datetime.strptime(str_date, '%Y.%m.%d')
    str_date = data[len(data)-1].date
    last = datetime.datetime.strptime(str_date, '%Y.%m.%d')
    max_delta = int((last-first).days)
    x = []
    avg_diff = []
    for d in data:
        str_dte = d.date
        dte = datetime.datetime.strptime(str_dte, '%Y.%m.%d')
        delta = int((last-dte).days)
        x.append(max_delta-delta)
        avg_diff.append(float(d.five_year))
    plt.plot(x, avg_diff, label=f'{type}')

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


def update_plt(idx_, category=""):
    file_name = f'{STR_NOW}_{category}{idx_}'
    file_path = f'media/{file_name}.png'
    plt.savefig(file_path)
    response= S3_CLIENT.upload_file(file_path, AWS_STORAGE_BUCKET_NAME, file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    print(f"updated: {file_name}")

# 주의***: 추후에 db의 가장 마지막 칼럼의 날짜의 파일을 삭제하도록 변경할 것
def delete_plt(idx_, date_, category=""):
    file_name = f'{date_}_{category}{idx_}' # STR_YST로 변경할 것 [12.10]
    file_path = f'media/{file_name}.png'
    response = S3_CLIENT.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_path)


def make_figure_plt(type_name, *funcs, term_num=4):
    plt.clf() # plt 초기화
    obj = _get_obj(type_name)
    terms = div_term(obj, term_num=term_num)
    x = [f"term{i+1}" for i in range(term_num)]
    for fi, func in enumerate(funcs):
        avg_diff = []
        label = func.__name__
        label = re.sub('snd_', '', label)
        for i, tr in enumerate(terms):
            obj_by_term = []
            for t in tr:
                obj_by_term.append(obj[t])
            value = round(func(obj_by_term), 5)
            avg_diff.append(value)
        plt.plot(x, avg_diff, label=label)
        for i, v in enumerate(x):
            plt.text(v, avg_diff[i], avg_diff[i], 
            rotation=fi%2*10, weight='bold')
    plt.legend()
    return plt


if __name__ == "__main__":
    # update plt 부분
    delete_date = '20211208'
    for i, value in enumerate(RATING_TYPE):
        plt.clf() # plt 초기화
        make_figure_plt(value, snd_avg_dff, snd_std_yld, snd_vol, snd_avg_yld)
        actPlot(value)
        update_plt(i)
        delete_plt(i, delete_date)
