# mongo-datatables Django Demo

A minimal Django app demonstrating server-side DataTables powered by
[mongo-datatables](https://github.com/pjosols/mongo-datatables).

## Quickstart

1. Clone and install:
   ```bash
   git clone https://github.com/pjosols/django-demo.git
   cd django-demo
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Seed the database (requires MongoDB running locally):
   ```bash
   python seed_data.py
   ```

3. Run:
   ```bash
   cd demo
   python manage.py runserver
   ```

Open [http://localhost:8000](http://localhost:8000).

## Custom MongoDB connection

```bash
python seed_data.py --connection "mongodb://user:password@host:port/"
```

Set `MONGO_URI` in the environment to point the app at a different instance.

## Project structure

```
django-demo/
├── demo/
│   ├── laureates/
│   │   ├── static/laureates/js/table.js   # DataTables init
│   │   ├── templates/laureates/index.html # page template
│   │   ├── tools/db_init.py               # index creation
│   │   ├── apps.py                        # app config + MongoDB startup
│   │   ├── urls.py                        # routes
│   │   └── views.py                       # views + API endpoint
│   ├── demo/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── data/laureates.json      # Nobel Prize data (1901–present)
├── seed_data.py             # loads data into MongoDB
└── requirements.txt
```

## How it works

`views.py` defines the data fields and passes the DataTables request to `mongo-datatables`:

```python
DATA_FIELDS = [
    DataField("name",          "string"),
    DataField("gender",        "string"),
    DataField("birth_country", "string"),
    DataField("year",          "number"),
    DataField("category",      "string"),
    DataField("motivation",    "string"),
    DataField("share",         "number"),
]

class LaureatesDataView(View):
    def post(self, request):
        data = json.loads(request.body)
        result = DataTables(_get_db(), "laureates", data, data_fields=DATA_FIELDS).get_rows()
        return JsonResponse(result)
```

`table.js` points DataTables at that endpoint:

```javascript
$('#laureates_table').DataTable({
    serverSide: true,
    ajax: {
        url: '/api/laureates',
        type: 'POST',
        contentType: 'application/json',
        data: function (d) { return JSON.stringify(d); }
    },
    columns: [
        { data: 'year' },
        { data: 'category' },
        { data: 'name' },
        // ...
    ]
});
```

That's the entire integration.

## License

MIT
