from django.urls import path
from . import views

app_name = 'laureates'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/places', views.PlacesDataView.as_view(), name='places_data'),
]
