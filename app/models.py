from peewee import Model, CharField, FloatField, AutoField, ForeignKeyField


class Car(Model):
    car_id = AutoField()
    car = CharField(unique=True)


class Duration(Model):
    duration_id = AutoField()
    start = CharField()
    end = CharField()
    duration = FloatField()


class Racer(Model):
    racer_id = AutoField()
    abbr = CharField(unique=True)
    name = CharField()
    car_id = ForeignKeyField(Car)
    duration_id = ForeignKeyField(Duration)
