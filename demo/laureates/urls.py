from django.urls import path
from . import views

app_name = 'laureates'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/laureates', views.LaureatesDataView.as_view(), name='laureates_data'),
]
