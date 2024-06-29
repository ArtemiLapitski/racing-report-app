from bs4 import BeautifulSoup
import json


wrong_order = {'order': "descending"}
wrong_order_json_error = {'message': "'descending' order argument is invalid. Only 'desc' and 'asc' are allowed."}
wrong_order_html_error = '"\'descending\' order argument is invalid. Only \'desc\' and \'asc\' are '\
        'allowed."\n'

wrong_format = {'format': "some_format"}
wrong_format_json_error = {'message': "'some_format' format argument is invalid. Only 'html' or 'json' are allowed."}

no_racers_in_db_json_error = {'message': 'Please add a racer to report.'}


def get_soup_html(response_data):
    soup = BeautifulSoup(response_data, 'html.parser')
    return soup


formats = {
    'json': {'format': 'json'},
    'html': {'format': 'html'}
}


extract_from_db = [
    ('SVF', 'Sebastian Vettel', 'FERRARI', 64.415),
    ('VBM', 'Valtteri Bottas', 'MERCEDES', 72.434),
    ('SVM', 'Stoffel Vandoorne', 'MCLAREN RENAULT', 72.463)
]

report_html = \
    "1. Sebastian Vettel | FERRARI | 1:04.415\n" \
    "2. Valtteri Bottas | MERCEDES | 1:12.434\n" \
    "3. Stoffel Vandoorne | MCLAREN RENAULT | 1:12.463"


def test_report_html(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('report')
    soup = get_soup_html(response.data)
    report = soup.find('div', class_='report').text.strip()
    assert report == report_html


report_desc_html = \
    "1. Stoffel Vandoorne | MCLAREN RENAULT | 1:12.463\n" \
    "2. Valtteri Bottas | MERCEDES | 1:12.434\n" \
    "3. Sebastian Vettel | FERRARI | 1:04.415"


def test_report_desc_html(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('report', query_string={'order':  'desc'})
    soup = get_soup_html(response.data)
    report = soup.find('div', class_='report').text.strip()
    assert report == report_desc_html


report_json = [
  {
    "abbr": "SVF",
    "name": "Sebastian Vettel",
    "position": 1,
    "car": "FERRARI",
    "result": "1:04.415"
  },
  {
    "abbr": "VBM",
    "name": "Valtteri Bottas",
    "position": 2,
    "car": "MERCEDES",
    "result": "1:12.434"
  },
  {
    "abbr": "SVM",
    "name": "Stoffel Vandoorne",
    "position": 3,
    "car": "MCLAREN RENAULT",
    "result": "1:12.463"
  }
    ]


def test_report_json(client, mocker):
    mocker.patch('app.api.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('api/report')
    assert response.content_type == 'application/json'
    report = json.loads(response.data)
    assert report == report_json


report_desc_json = [
  {
    "abbr": "SVM",
    "name": "Stoffel Vandoorne",
    "position": 1,
    "car": "MCLAREN RENAULT",
    "result": "1:12.463"
  },
  {
    "abbr": "VBM",
    "name": "Valtteri Bottas",
    "position": 2,
    "car": "MERCEDES",
    "result": "1:12.434"
  },
  {
    "abbr": "SVF",
    "name": "Sebastian Vettel",
    "position": 3,
    "car": "FERRARI",
    "result": "1:04.415"
  }
    ]


def test_report_desc_json(client, mocker):
    mocker.patch('app.api.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('api/report', query_string={'order': 'desc'})
    assert response.content_type == 'application/json'
    report = json.loads(response.data)
    assert report == report_desc_json


def test_report_wrong_order_error(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('report', query_string=wrong_order)
    soup = get_soup_html(response.data)
    assert soup.get_text() == wrong_order_html_error


def test_report_no_racers_in_db_json_error(client, mocker):
    mocker.patch('app.api.views.check_records_in_db', return_value=False)
    response = client.get('api/report')
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data_dict = json.loads(response.data)
    assert data_dict == no_racers_in_db_json_error


def test_report_no_racers_in_db_status_code_html(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=False)
    response = client.get('report')
    assert response.status_code == 302


drivers_html = \
    "SVF - Sebastian Vettel \n" \
    "VBM - Valtteri Bottas \n" \
    "SVM - Stoffel Vandoorne"


def test_drivers_html(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('report/drivers')
    soup = get_soup_html(response.data)
    report = soup.find('div', class_='drivers').text.strip()
    assert report == drivers_html


def test_drivers_wrong_order_error(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    response = client.get('report/drivers', query_string=wrong_order)
    soup = get_soup_html(response.data)
    assert soup.get_text() == wrong_order_html_error


def test_drivers_no_racers_in_db_status_code_html(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=False)
    response = client.get('report/drivers')
    assert response.status_code == 302


drivers_stat_mock = \
 'Statistics on Sebastian Vettel:\n'\
 'Position: 1\n'\
 'Time: 1:04.415\n'\
 'Car: FERRARI\n'\
 'Abbreviation: SVF'


def test_driver_stat_SVF_html(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('report/drivers/SVF')
    soup = get_soup_html(response.data)
    driver_stat = soup.find('div', class_='driver_stat').text.strip()
    assert driver_stat == drivers_stat_mock


driver_SVF_desc_mock = \
 'Statistics on Sebastian Vettel:\n'\
 'Position: 3\n'\
 'Time: 1:04.415\n'\
 'Car: FERRARI\n'\
 'Abbreviation: SVF'


def test_driver_stat_SVF_desc_html(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('report/drivers/SVF', query_string={'order': 'desc'})
    soup = get_soup_html(response.data)
    driver_stat = soup.find('div', class_='driver_stat').text.strip()
    assert driver_stat == driver_SVF_desc_mock


driver_stat_SVF = [
    {"abbr": "SVF",
     "name": "Sebastian Vettel",
     "position": 1,
     "car": "FERRARI",
     "result": "1:04.415"}
]


def test_driver_stat_SVF_json(client, mocker):
    mocker.patch('app.api.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('api/report/drivers/SVF')
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert data == driver_stat_SVF


driver_stat_SVF_desc = [
    {"abbr": "SVF",
     "name": "Sebastian Vettel",
     "position": 3,
     "car": "FERRARI",
     "result": "1:04.415"}
]


def test_driver_stat_SVF_desc_json(client, mocker):
    mocker.patch('app.api.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('api/report/drivers/SVF', query_string={'order': 'desc'})
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert data == driver_stat_SVF_desc


wrong_driver_error_message = {'message': "'SVFF' driver id was not found."}


def test_driver_stat_wrong_driver_id_error(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('report/drivers/SVFF')
    soup = get_soup_html(response.data)
    assert soup.get_text() == '"\'SVFF\' driver id was not found."\n'


def test_driver_stat_wrong_order_error(client, mocker):
    mocker.patch('app.templates.views.check_records_in_db', return_value=True)
    response = client.get('report/drivers/SVF', query_string=wrong_order)
    soup = get_soup_html(response.data)
    assert soup.get_text() == wrong_order_html_error
