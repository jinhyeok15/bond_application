import boto3
from bondproject.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME

import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bondproject.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
from bondapp.models import BondYld

from matplotlib import pyplot as plt
import numpy as np
import datetime
import math


def makePlot(type):
    data = BondYld.objects.filter(bond_type=type)
    now = datetime.datetime.now()
    str_first = data[0].date
    first = datetime.datetime.strptime(str_first, '%Y.%m.%d')
    max_delta = int((now-first).days)
    x = []
    y = []
    for d in data:
        str_dte = d.date
        dte = datetime.datetime.strptime(str_dte, '%Y.%m.%d')
        delta = int((now-dte).days)
        x.append(max_delta-delta)
        y.append(float(d.five_year))
    plt.plot(x, y)
    plt.yticks(np.arange(0, 3, 0.5))
    x_date = []
    arr_days = np.arange(0, max_delta+1, int(math.floor((max_delta+1)/4)))
    for nday in  arr_days:
        nday=int(nday)
        tme_delta = datetime.timedelta(days=nday)
        x_date.append((first+tme_delta).strftime('%Y.%m.%d'))
    plt.xticks(arr_days, x_date)
    
    return plt

client = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME
                      )
response = client.list_buckets() # bucket 목록

plot = makePlot('국고채')
plot.show()
