from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import DataRequired
from .form_validations import car_validation, name_validation_no_space, name_validation_chars_and_spaces_only, \
    abbr_validation_chars_only, abbr_validation_upper_chars, abbr_validation_is_in_db
from wtforms.fields import DateTimeField
from app.config import DATETIME_FORMAT


class CreateRacerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), name_validation_no_space,
                                           name_validation_chars_and_spaces_only, validators.Length(min=4, max=25)])
    abbr = StringField('Abbreviation', validators=[DataRequired(), abbr_validation_is_in_db,
                                                   abbr_validation_upper_chars, abbr_validation_chars_only,
                                                   validators.Length(min=3, max=3)])
    car = StringField('Car', validators=[DataRequired(), car_validation, validators.Length(min=3, max=25)])
    start = DateTimeField('Start', format=DATETIME_FORMAT)
    end = DateTimeField('End', format=DATETIME_FORMAT)
