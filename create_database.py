from app.database import db
from app.models import Racer, Car, Duration
from os import mkdir
from app.config import DATABASE_FOLDER


if __name__ == "__main__":
    mkdir(DATABASE_FOLDER)
    db.create_tables([Racer, Car, Duration])
