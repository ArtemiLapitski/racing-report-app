from pydantic import BaseModel, validator, constr
from .schemas_validations import name_validation, abbr_validation, car_validation, \
    end_after_start_validation, end_race_validation, start_race_validation, order_validation
from datetime import datetime
from typing import Optional


class RacerToCreate(BaseModel):
    name: constr(min_length=4, max_length=25)
    abbr: constr(min_length=3, max_length=3)
    car: constr(min_length=3, max_length=25)
    start: datetime
    end: datetime

    validate_name = validator('name')(name_validation)
    validate_abbr = validator('abbr')(abbr_validation)
    validate_car = validator('car')(car_validation)
    validate_start = validator('start', pre=True)(start_race_validation)
    validate_end = validator('end', pre=True)(end_race_validation)
    validate_end_after_start = validator('end')(end_after_start_validation)


class RacerToRetrieve(BaseModel):
    name: str
    abbr: str
    car: str
    start: str
    end: str

    @classmethod
    def get_racer_to_retrieve(cls, racer):
        return cls(
            name=racer.name,
            abbr=racer.abbr,
            car=racer.car_id.car,
            start=racer.duration_id.start,
            end=racer.duration_id.end
        )


class OrderToValidate(BaseModel):
    order: Optional[str] = False

    validate_order = validator('order')(order_validation)
