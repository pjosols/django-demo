$(function () {
    $('#laureates_table').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/api/laureates',
            type: 'POST',
            contentType: 'application/json',
            data: function (d) { return JSON.stringify(d); }
        },
        order: [[0, 'desc']],
        columns: [
            { data: 'year',          width: '70px' },
            { data: 'category',      width: '110px' },
            { data: 'name',          width: '160px' },
            { data: 'birth_country', width: '140px', defaultContent: '—' },
            { data: 'share',         width: '60px', className: 'dt-center' },
            {
                data: 'motivation',
                defaultContent: '—',
                render: function (data) {
                    if (!data) return '—';
                    return data.length > 80 ? data.substring(0, 80) + '…' : data;
                }
            },
        ]
    });
});
