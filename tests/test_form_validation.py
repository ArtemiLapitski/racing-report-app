from app.models import Racer, Car, Duration
from .test_app import get_soup_html
import pytest
from .test_database import racer_data_example

MODELS = [Racer, Car, Duration]


params = [
    (
        {'name': 'Sebastian'},
        'Error: name must contain a space'
    ),
    (
        {'name': 'Sebastian !'},
        'Error: name must contain letters and whitespaces only'
    ),
    (
        {'name': 'Sebastian!'},
        'Error: name must contain a space Error: name must contain letters and whitespaces only'
    ),
    (
        {
            'abbr': 'pi ',
            'name': 'Sebastian Vettel'
        },
        'Error: all letters must be uppercase Error: abbreviation can contain letters only'
    ),
    (
        {
            'abbr': 'pi!',
            'name': 'Sebastian Vettel'
        },
        'Error: all letters must be uppercase Error: abbreviation can contain letters only'
    ),
    (
        {
            'abbr': 'pio',
            'name': 'Sebastian Vettel'
        },
        'Error: all letters must be uppercase'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'car': 'FERRARI!',
            'abbr': 'SVF'
        },
        'Error: car must not contain special characters'
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'car': 'FERRARI',
            'abbr': 'SVF',
            'start': '2018-5-24 12:4:2.979'
        },
        "Error: Not a valid datetime value."
    ),
    (
        {
            'name': 'Sebastian Vettel',
            'car': 'FERRARI',
            'abbr': 'SVF',
            'end': '2018-5-24 12:4:2.979'
        },
        "Error: Not a valid datetime value."
    )
]


@pytest.mark.parametrize('input, error', params)
def test_form_errors(client, input, error):
    response = client.post('add_driver', data=input)
    soup = get_soup_html(response.data)
    output = soup.find('div', class_='errors').text.strip()
    output = output.replace("\n", "")
    output = output.replace("                                                                    ", " ")
    assert output == error


def test_form_abbr_exists_in_db_error(client):
    client.post('/api/driver', json=racer_data_example)
    response = client.post('add_driver', data=racer_data_example)
    soup = get_soup_html(response.data)
    output = soup.find('div', class_='errors').text.strip()
    assert output == "Error: Racer with 'SVF' abbreviation already exists"
