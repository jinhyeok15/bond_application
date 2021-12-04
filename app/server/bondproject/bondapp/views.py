from django.shortcuts import render

# Create your views here.

def home_template(request):
    default_type = {"국고채":"KTB"}
    return render(request, 'home/home.html', {"defaultType": default_type})
