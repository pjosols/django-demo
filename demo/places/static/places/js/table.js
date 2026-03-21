$(function () {

    const headerToKey = {
        'name':       'name',
        'country':    'country_code',
        'feature':    'feature_code',
        'region':     'admin1_code',
        'population': 'population',
        'timezone':   'timezone',
    };

    function remapSearch(value) {
        return value.replace(/(\w+):/gi, function (match, word) {
            const key = headerToKey[word.toLowerCase()];
            return key ? key + ':' : match;
        });
    }

    $('#places_table').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/api/places',
            type: 'POST',
            contentType: 'application/json',
            data: function (d) {
                if (d.search && d.search.value) {
                    d.search.value = remapSearch(d.search.value);
                }
                return JSON.stringify(d);
            }
        },
        orderCellsTop: true,
        order: [[4, 'desc']],
        initComplete: function () {
            var api = this.api();
            var row = $('<tr class="col-search-row">').appendTo('#places_table thead');
            api.columns().every(function () {
                var col = this;
                var title = $(col.header(0)).text().trim();
                var placeholders = {
                    'Name': 'New York', 'Country': 'US', 'Feature': 'PPL',
                    'Region': 'NY', 'Population': '>1000000', 'Timezone': 'America/New_York'
                };
                $('<th>').appendTo(row).append(
                    $('<input type="text">').attr('placeholder', placeholders[title] || title)
                        .on('input', function () {
                            col.search(this.value).draw();
                        })
                );
            });
        },
        columns: [
            { data: 'name',          width: '180px' },
            { data: 'country_code',  width: '80px',  className: 'dt-center' },
            { data: 'feature_code',  width: '90px',  className: 'dt-center', defaultContent: '—' },
            { data: 'admin1_code',   width: '90px',  className: 'dt-center', defaultContent: '—' },
            {
                data: 'population',
                width: '110px',
                className: 'dt-right',
                defaultContent: '—',
                render: function (data) {
                    if (!data) return '—';
                    return data.toLocaleString();
                }
            },
            { data: 'timezone', width: '160px', defaultContent: '—' },
        ]
    });
});
