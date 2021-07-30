from django.urls import path
from . import views

urlpatterns = [
    path('see-data', views.index),
    path('', views.base)
]