from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class VisualView(View):
    def get(self, request):
        return render(request, 'visual.html', {})

    def post(self, request):
        pass

def get_data(request):
    data = {
        'sales': 100,
        'customer': 10,
    }
    return JsonResponse(data)