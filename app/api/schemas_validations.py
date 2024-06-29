from datetime import datetime
from app.database import abbr_is_in_db
from app.config import DATETIME_FORMAT


def check_for_spec_chars(string: str) -> bool:
    return any(not c.isalnum() for c in string.replace(' ', ''))


def check_letters_and_whitespace_only(string: str) -> bool:
    return not string.replace(' ', '').isalpha()


def name_validation(cls, v):
    name = v.strip()
    if check_letters_and_whitespace_only(name):
        raise ValueError('name must contain letters and whitespaces only')
    elif ' ' not in name:
        raise ValueError('name must contain a space')
    return name.title()


def abbr_validation(cls, v):
    if abbr_is_in_db(v):
        raise ValueError(f"Racer with '{v}' abbreviation already exists")
    elif not v.isalpha():
        raise ValueError('abbreviation must contain only letters')
    return v.strip().upper()


def car_validation(cls, v):
    if check_for_spec_chars(v):
        raise ValueError('car must not contain special characters')
    return v.strip().upper()


def start_race_validation(cls, v):
    try:
        start_datetime = datetime.strptime(v, DATETIME_FORMAT)
    except ValueError:
        raise ValueError(f"start time of the race {v} does not match format 2017-05-24_12:01:58.937")
    return start_datetime


def end_after_start_validation(cls, v, values):
    try:
        start_datetime = values['start']
        if v < start_datetime:
            raise ValueError(f"end of the race should happen after the start")
        return v
    except KeyError:
        pass


def end_race_validation(cls, v):
    try:
        end_datetime = datetime.strptime(v, DATETIME_FORMAT)
    except ValueError:
        raise ValueError(f"end time of the race {v} does not match format 2017-05-24_12:01:58.937")
    return end_datetime


def order_validation(cls, v):
    if v not in ('desc', 'asc'):
        raise ValueError(f"'{v}' order argument is invalid. Only 'desc' and 'asc' are allowed.")
    elif v == "desc":
        return True
    else:
        return False
