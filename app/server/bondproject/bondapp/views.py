from django.shortcuts import render
from .models import BondYld
from .req.kis import RATING_TYPE
from bondproject.settings import (
    AWS_S3_CUSTOM_DOMAIN
)
from .fin.figure import *
import re
import datetime

# Create your views here.
S3_PATH = 'https://'+AWS_S3_CUSTOM_DOMAIN+f'/media/'
NOW_DATE = '20211214'


def home_template(request):
    template = 'home/home.html'
    DEFAULT_TYPE = "국고채"
    S3_DEFAULT_URL = 'https://'+AWS_S3_CUSTOM_DOMAIN+f'/media/20211214_0.png'
    TERM_UNIT = 4
    
    if request.method == "GET":
        provide = {
            "types": RATING_TYPE,
            "selected_type": DEFAULT_TYPE,
            "source": S3_DEFAULT_URL,
            "tab": '0',
        }
        return render(request, template, provide)

    if request.method == "POST":
        # rate
        rate_type = request.POST['type']
        rate_idx = RATING_TYPE.index(rate_type)
        rate_s3_path = S3_PATH + NOW_DATE +f'_{rate_idx}.png'

        ordered_type = list(map(lambda x: x, RATING_TYPE))
        ordered_type.remove(rate_type)
        ordered_type.insert(0, rate_type)

        # tab
        tab_type = request.POST['tab']

        # figure
        figure_s3_path = S3_PATH + NOW_DATE +f'_figure{rate_idx}.png'
        
        provide = {
            "types": ordered_type,
            "selected_type": rate_type,
            "source": rate_s3_path,
            'tab': tab_type,
            'figure_source': figure_s3_path,
        }
        return render(request, template, provide)


def test(request):
    return render(request, 'test.html')
