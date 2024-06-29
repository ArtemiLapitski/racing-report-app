from wtforms.validators import ValidationError
from app.api.schemas_validations import check_for_spec_chars, check_letters_and_whitespace_only
from app.database import abbr_is_in_db


def name_validation_chars_and_spaces_only(form, field):
    name = field.data.strip()
    if check_letters_and_whitespace_only(name):
        raise ValidationError('name must contain letters and whitespaces only')


def name_validation_no_space(form, field):
    name = field.data.strip()
    if ' ' not in name:
        raise ValidationError('name must contain a space')


def abbr_validation_is_in_db(form, field):
    abbr = field.data
    if abbr_is_in_db(abbr):
        raise ValidationError(f"Racer with '{abbr}' abbreviation already exists")


def abbr_validation_chars_only(form, field):
    abbr = field.data
    if not abbr.isalpha():
        raise ValidationError('abbreviation can contain letters only')


def abbr_validation_upper_chars(form, field):
    abbr = field.data
    if not abbr.isupper():
        raise ValidationError('all letters must be uppercase')


def car_validation(form, field):
    if check_for_spec_chars(field.data):
        raise ValidationError('car must not contain special characters')
