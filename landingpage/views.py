from django.shortcuts import render

# Create your views here.
def mobile(request):
    return render(request, 'landingpage/mobile.html')
