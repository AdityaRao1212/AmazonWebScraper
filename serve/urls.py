from django.urls import path
from . import views

urlpatterns = [
    path('see-data', views.index, name='see-data'),
    path('', views.base, name='home')
]