from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Scraped
from .new_scrap import Scrapper

# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cat = request.POST.get('cat')
        pages = request.POST.get('pages')

        scrapper = Scrapper(name, cat, pages)
        df = scrapper.scrap()
        
        for i in range(len(df)):
            Scraped.objects.create(
                user_name=name, 
                brands=df.iloc[i, 1] ,
                categories=df.iloc[i, 2],
                names=df.iloc[i, 3],
                rating=float(df.iloc[i, 4]),
                total_rating=int(df.iloc[i, 5]),
                cost_price=int(float(df.iloc[i, 6])),
                selling_price=int(float(df.iloc[i, 7])),
                discount=int(float(df.iloc[i, 8])),
                discount_per=int(df.iloc[i, 9]),
                links=df.iloc[i, 10]
            )

        data = Scraped.objects.filter(user_name=name)
        return render(request, 'data.html', {'data': data})
    # return HttpResponseRedirect('/')
    # data = Scraped.objects.all()
    # return render(request, 'data.html', {'data': data})

def base(request):
    return render(request, 'index.html')

# def get_data(request):
#     # Create DataFrame
#     # Convert into Excel or csv
#     pass