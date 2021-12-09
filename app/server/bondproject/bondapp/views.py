from django.shortcuts import render
from .models import BondYld
from .req.kis import RATING_TYPE
from bondproject.settings import (
    AWS_S3_CUSTOM_DOMAIN
)
from .fin.figure import *
import re

# Create your views here.


def home_template(request):
    template = 'home/home.html'
    DEFAULT_TYPE = "국고채"
    S3_DEFAULT_URL = 'https://'+AWS_S3_CUSTOM_DOMAIN+f'/media/20211208_{DEFAULT_TYPE}.png'
    TERM_UNIT = 4
    
    if request.method == "GET":
        provide = {
            "types": RATING_TYPE,
            "source": S3_DEFAULT_URL,
            "selected_type": DEFAULT_TYPE,
            "tab": '0',
        }
        return render(request, template, provide)

    if request.method == "POST":
        # rate
        rate_type = request.POST['type']
        sub_type = re.sub('[+]', 'p', rate_type)
        sub_type = re.sub('[-]', 'm', sub_type)
        s3_url = 'https://'+AWS_S3_CUSTOM_DOMAIN+f'/media/20211208_{sub_type}.png'

        ordered_type = list(map(lambda x: x, RATING_TYPE))
        ordered_type.remove(rate_type)
        ordered_type.insert(0, rate_type)

        # tab
        tab_type = request.POST['tab']

        # figure
        obj = BondYld.objects.filter(bond_type=rate_type)
        terms = div_term(obj, term_num=TERM_UNIT)
        figs = []
        for i, tr in enumerate(terms):
            obj_by_term = []
            for t in tr:
                obj_by_term.append(obj[t])
            figs.append({
                "term": str(i+1),
                "vol": str(snd_vol(obj_by_term)),
                "diff": str(snd_avg_dff(obj_by_term)),
            })
        
        provide = {
            "types": ordered_type,
            "source": s3_url,
            "selected_type": rate_type,
            'tab': tab_type,
            'figure': figs,
        }
        return render(request, template, provide)


def test(request):
    return render(request, 'test.html')
