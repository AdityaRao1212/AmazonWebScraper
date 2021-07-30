from django.shortcuts import render
from .models import Scraped

# Create your views here.
def index(request):
    data = Scraped.objects.all()
    return render(request, 'data.html', {'data': data})

def base(request):
    return render(request, 'index.html')