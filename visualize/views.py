from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response

from serve.models import FastScraped

import json as j
import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
class VisualView(View):
    def get(self, request, name):
        return render(request, 'visual.html', {'name': name})

    def post(self, request):
        pass


class GetData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = {
        'sales': 100,
        'customer': 10,
        }
        return Response(data)

    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        body = j.loads(body_unicode)
        name = body['name']
        rows = int(body['rows'])
        radio = body['radio']
        to_asc = body['to_asc']
        csv_path = BASE_DIR + '/csv/' + name + '.csv'
        df = pd.read_csv(csv_path, encoding='cp1252')
        df = get_data(df, rows, radio, to_asc)
        json_data = df.to_json()
        return Response(json_data)

def get_data(df, rows, col, is_asc):
    df = df[['names', col]]
    new_df = df.sort_values(col, ascending=is_asc)
    new_df = new_df.iloc[:rows]
    new_df.index = [i for i in range(rows)]
    new_df['names'] = new_df['names'].map(lambda x:' '.join((x.split()[:5])))
    return new_df