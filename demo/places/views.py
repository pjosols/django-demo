import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from mongo_datatables import DataTables, DataField


DATA_FIELDS = [
    DataField("name",         "string"),
    DataField("country_code", "keyword"),
    DataField("feature_code", "keyword"),
    DataField("admin1_code",  "keyword"),
    DataField("population",   "number"),
    DataField("timezone",     "string"),
    DataField("latitude",     "number"),
    DataField("longitude",    "number"),
]


_client = None


def _get_db():
    global _client
    if _client is None:
        _client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
    return _client['geonames_demo']


class IndexView(View):
    def get(self, request):
        return render(request, 'places/index.html')


@method_decorator(csrf_exempt, name='dispatch')
class PlacesDataView(View):
    def post(self, request):
        data = {}
        try:
            data = json.loads(request.body)
            result = DataTables(_get_db(), "places", data, data_fields=DATA_FIELDS).get_rows()
            return JsonResponse(result)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'error': str(e), 'data': [],
                'draw': data.get('draw', 1),
                'recordsTotal': 0, 'recordsFiltered': 0
            }, status=500)
