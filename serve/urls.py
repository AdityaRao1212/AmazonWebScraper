from django.urls import path
from . import views

urlpatterns = [
    path('full-data', views.index, name='see-data'),
    path('', views.base, name='home'),
    path('download/<str:filename>', views.download_file, name='download_file'),
]