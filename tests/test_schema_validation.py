import pytest
from .test_database import racer_data_example


params = [
    (
        {
            'name': 'SebastianVettel',
            'abbr': 'SVF',
            'car': 'FERRARI',
            'start': '2018-05-24_12:02:58.917',
            'end': '2018-05-24_12:04:03.332'
        },
        b'{'
        b'"validation_error":{"body_params":[{"loc":["name"],"msg":"name must contain a space","type":"value_error"}]}'
        b'}\n'
    ),
    (
        {
            'name': 'Sebastian Vettel!',
            'abbr': 'SVF',
            'car': 'FERRARI',
            'start': '2018-05-24_12:02:58.917',
            'end': '2018-05-24_12:04:03.332'
        },
        b'{'
        b'"validation_error":{"body_params":[{"loc":["name"],"msg":"name must contain letters and whitespaces only",'
        b'"type":"value_error"}]}'
        b'}\n'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'abbr': 'SV!',
            'car': 'FERRARI',
            'start': '2018-05-24_12:02:58.917',
            'end': '2018-05-24_12:04:03.332'
        },
        b'{'
        b'"validation_error":{"body_params":[{"loc":["abbr"],"msg":"abbreviation must contain only letters",'
        b'"type":"value_error"}]}'
        b'}\n'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'abbr': 'SV',
            'car': 'FERRARI',
            'start': '2018-05-24_12:02:58.917',
            'end': '2018-05-24_12:04:03.332'
        },
        b'{"validation_error":{"body_params":[{"ctx":{"limit_value":3},"loc":["abbr"],'
        b'"msg":"ensure this value has at least 3 characters","type":"value_error.any_str.min_length"}]}}\n'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'abbr': 'SVF',
            'car': 'FERRARI!',
            'start': '2018-05-24_12:02:58.917',
            'end': '2018-05-24_12:04:03.332'
        },
        b'{"validation_error":{"body_params":[{"loc":["car"],"msg":"car must not contain special characters",'
        b'"type":"value_error"}]}}\n'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'abbr': 'SVF',
            'car': 'FERRARI',
            'start': '2018',
            'end': '2018-05-24_12:04:03.332'
        },
        b'{"validation_error":{"body_params":[{"loc":["start"],"msg":"start time of the race 2018 does not match format'
        b' 2017-05-24_12:01:58.937","type":"value_error"}]}}\n'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'abbr': 'SVF',
            'car': 'FERRARI',
            'start': '2018-05-24_12:04:03.332',
            'end': '2018'
        },
        b'{"validation_error":{"body_params":[{"loc":["end"],"msg":"end time of the race 2018 does not match format '
        b'2017-05-24_12:01:58.937","type":"value_error"}]}}\n'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'abbr': 'SVF',
            'car': 'FERRARI',
            'start': '2018-05-24_12:04:03.332',
            'end': '2018-05-24_12:04:03.3'
        },
        b'{"validation_error":{"body_params":[{"loc":["end"],"msg":"end of the race should happen after the start",'
        b'"type":"value_error"}]}}\n'
    )
]


@pytest.mark.parametrize('racer_data, error', params)
def test_schema_validation_errors(client, racer_data, error):
    response = client.post('/api/driver', json=racer_data)
    assert response.data == error


abbr_already_exists_error = b'{"validation_error":{"body_params":[{"loc":["abbr"],"msg":"Racer with \'SVF\'' \
                            b' abbreviation already exists","type":"value_error"}]}}\n'


def test_schema_abbr_already_exists_error(client):
    client.post('/api/driver', json=racer_data_example)
    response = client.post('/api/driver', json=racer_data_example)
    assert response.data == abbr_already_exists_error


wrong_order_error = b'{"validation_error":{"query_params":[{"loc":["order"],' \
                    b'"msg":"\'descc\' order argument is invalid. Only \'desc\' and \'asc\' are allowed.",' \
                    b'"type":"value_error"}]}}\n'


def test_schema_report_wrong_order_error(client, mocker):
    mocker.patch('app.api.views.check_records_in_db', return_value=True)
    response = client.get('api/report', query_string={'order': 'descc'})
    assert response.data == wrong_order_error


def test_schema_one_driver_wrong_order_error(client, mocker):
    mocker.patch('app.api.views.check_records_in_db', return_value=True)
    response = client.get('api/report', query_string={'order': 'descc'})
    assert response.data == wrong_order_error
