from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response

from serve.models import FastScraped

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

    def post(self, request):
        name = request.POST.get('name')
        csv_path = BASE_DIR + '/csv/' + name + '.csv'
        df = pd.read_csv(csv_path, encoding='cp1252')[:1]
        json = df.to_json()
        return Response(json)