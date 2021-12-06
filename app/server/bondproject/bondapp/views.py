from django.shortcuts import render
from .models import BondYld
from .req.kis import RATING_TYPE
from bondproject.settings import (
    AWS_S3_CUSTOM_DOMAIN
)

# Create your views here.
def home_template(request):
    default_type = {"국고채":"KTB"}
    URL = 'https://'+AWS_S3_CUSTOM_DOMAIN+'/media/sample_img.jpg'
    provide = {
        "defaultType": default_type,
        "types": RATING_TYPE,
        "source": URL
    }
    return render(request, 'home/home.html', provide)
