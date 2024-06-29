from app.models import Racer, Car, Duration
from app.database import check_records_in_db
import json


MODELS = [Racer, Car, Duration]

racer_data_example = {
    'name': 'Sebastian Vettel',
    'abbr': 'SVF',
    'car': 'FERRARI',
    'start': '2018-05-24_12:02:58.917',
    'end': '2018-05-24_12:04:03.332'
}

response_racer_created = b'{' \
                         b'"name": "Sebastian Vettel",' \
                         b' "abbr": "SVF",' \
                         b' "car": "FERRARI",' \
                         b' "start": "2018-05-24 12:02:58.917000",' \
                         b' "end": "2018-05-24 12:04:03.332000"' \
                         b'}\n'


def test_database_create_racer(client):
    assert check_records_in_db() == False
    response = client.post('/api/driver', json=racer_data_example)
    assert response.status_code == 201
    assert response.data == response_racer_created
    assert check_records_in_db() == True


report_json = [
  {
    "abbr": "SVF",
    "name": "Sebastian Vettel",
    "position": 1,
    "car": "FERRARI",
    "result": "1:04.415"
  }
]


def test_database_extract_racer_from_bd(client):
    client.post('/api/driver', json=racer_data_example)
    response = client.get('/api/report')
    report = json.loads(response.data)
    assert report == report_json
