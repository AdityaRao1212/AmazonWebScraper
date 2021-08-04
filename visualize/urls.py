from django.urls import path
from . import views


urlpatterns = [
    path('<str:name>', views.VisualView.as_view(), name='visualize'),
    path('api/getdata/', views.GetData.as_view(), name='api-getdata')
]