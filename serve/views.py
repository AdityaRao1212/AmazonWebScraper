import mimetypes
import os
import csv
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Scraped, FastScraped
from .slow_scrap import Scrapper
from .fast_scrap import FastScrapper
from .debug_utils import debug

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cat = request.POST.get('cat')
        pages = request.POST.get('pages')
        radio = request.POST.get('radio')

        if radio == 'slow':
            scrapper = Scrapper(name, cat, pages)
            df = scrapper.scrap()
            for i in range(len(df)):
                try:
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
                except:
                    continue
            data = Scraped.objects.filter(user_name=name)
            data_to_write = Scraped.objects.filter(user_name=name).values_list('brands', 'categories', 'names', 'rating', 'total_rating', 'cost_price', 'selling_price', 'discount', 'discount_per','links')
            
            csv_name = f"{name}.csv"
            csv_file_path = f"{BASE_DIR}/csv/{csv_name}"

            with open(csv_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, newline='')
                writer.writerow(['brands', 'categories', 'names', 'rating', 'total_rating', 'cost_price', 'selling_price', 'discount', 'discount_per','links'])
                for col in data_to_write:
                    writer.writerow(col)
            return render(request, 'data.html', {'data': data, 'name':name, 'csv_name': csv_name})

        elif radio == 'fast':
            scrapper = FastScrapper(name, cat, pages)
            df = scrapper.scrap()
            for i in range(len(df)):
                try:
                    FastScraped.objects.create(
                        user_name=name, 
                        categories=df.iloc[i, 1] ,
                        names=df.iloc[i, 2],
                        rating=float(df.iloc[i, 3]),
                        total_rating=int(float(df.iloc[i, 4])),
                        cost_price=int(float(df.iloc[i, 5])),
                        selling_price=int(float(df.iloc[i, 6])),
                        links=df.iloc[i, 7]
                    )
                except Exception as e:
                    #debug(type='e', message=e.__traceback__)
                    #debug(type='w', message='Exception Occurred, while creating FastScrapped object.')
                    continue
            data = FastScraped.objects.filter(user_name=name, categories=cat)
            for key, row in enumerate(data.values(), start=1):
                row['id'] = key
            data_to_write = FastScraped.objects.filter(user_name=name, categories=cat).values_list('categories', 'names', 'rating', 'total_rating', 'cost_price', 'selling_price', 'links')

            csv_name = f"{name}.csv"
            csv_file_path = f"{BASE_DIR}/csv/{csv_name}"

            with open(csv_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['categories', 'names', 'rating', 'total_rating', 'cost_price', 'selling_price', 'links'])
                for col in data_to_write:
                    writer.writerow(col)
            print()
            return render(request, 'fast_data.html', {'data': data, 'name':name, 'csv_name': csv_name})
    # return HttpResponseRedirect('/')
    #data = FastScraped.objects.all()
    return render(request, 'fast_data.html', {'data': {}})


def base(request):
    return render(request, 'index.html')


def download_file(request, filename):
    if filename != '':
        # Define the full file path
        filepath = BASE_DIR + '\\csv\\' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'index.html')