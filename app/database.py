from peewee import SqliteDatabase
from app.config import DATABASE_FOLDER, DATABASE_FILE
from pathlib import Path
from app.models import Racer, Car, Duration
from datetime import datetime
from peewee import Model

database_path = Path(DATABASE_FOLDER) / DATABASE_FILE
MODELS = [Racer, Car, Duration]


def connect_db():
    db = SqliteDatabase(database_path)
    db.bind(MODELS)
    return db


db = connect_db()


def check_records_in_db() -> bool:
    records = [
        bool(Racer.get_or_none(1)),
        bool(Car.get_or_none(1)),
        bool(Duration.get_or_none(1))
    ]
    return all(records)


def extract_from_db() -> list:
    query = (
        Racer.select(Racer, Car, Duration)
        .join(Car, on=(Racer.car_id == Car.car_id))
        .join(Duration, on=(Racer.duration_id == Duration.duration_id))
    )

    data = [(racer.abbr, racer.name, racer.car, racer.duration) for racer in query.objects()]

    return data


def abbr_is_in_db(abbr: str) -> bool:
    query = Racer.select().where(Racer.abbr == abbr)
    if query.exists():
        return True
    else:
        return False


def car_is_in_db(car: str) -> bool:
    query = Car.select().where(Car.car == car)
    if query.exists():
        return True
    else:
        return False


def create_racer(name: str, abbr: str, car: str, start: datetime, end: datetime):
    car_id, _ = Car.get_or_create(car=car)
    duration = (end - start).total_seconds()
    new_duration = Duration.create(start=start, end=end, duration=duration)
    return Racer.create(name=name, abbr=abbr, car_id=car_id, duration_id=new_duration.duration_id)


def get_racer_from_db(racer: Model):
    return Racer.select() \
        .join(Car, on=(Racer.car_id == Car.car_id)) \
        .join(Duration, on=(Racer.duration_id == Duration.duration_id))\
        .where(Racer.racer_id == racer.racer_id) \
        .get()
