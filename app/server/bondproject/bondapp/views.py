from django.shortcuts import render

from .req.kis import RATING_TYPE

# Create your views here.

def home_template(request):
    default_type = {"국고채":"KTB"}
    return render(request, 'home/home.html', {"defaultType": default_type, "types": RATING_TYPE})
