from flask import abort
from flask_restful import Resource
from flasgger import swag_from
from app.database import create_racer, check_records_in_db, get_racer_from_db
from app.api.schemas import RacerToCreate, RacerToRetrieve,OrderToValidate
from report import generate_report_from_db, report_to_list, DriverNotFound
from app.config import API_REPORT_SWAGGER_PATH, API_ADD_DRIVER_SWAGGER_PATH, API_ONE_DRIVER_SWAGGER_PATH
from flask_pydantic import validate


def check_order(order: str = None) -> bool:
    if order and order not in ('desc', 'asc'):
        abort(400, f"'{order}' order argument is invalid. Only 'desc' and 'asc' are allowed.")
    elif order == "desc":
        reverse = True
    else:
        reverse = False
    return reverse


def check_records(func):
    def wrapper(*args, **kwargs):

        if not check_records_in_db():
            abort(400, "Please add a racer to report.")

        return func(*args, **kwargs)
    return wrapper


class ApiAddDriverResource(Resource):

    @swag_from(API_ADD_DRIVER_SWAGGER_PATH)
    @validate()
    def post(self, body: RacerToCreate):
        created_racer = create_racer(**body.dict())
        racer_from_db = get_racer_from_db(created_racer)
        return RacerToRetrieve.get_racer_to_retrieve(racer_from_db).dict(), 201


class ApiReportResource(Resource):

    @swag_from(API_REPORT_SWAGGER_PATH)
    @check_records
    @validate()
    def get(self, query: OrderToValidate):
        order = query.order
        report = generate_report_from_db(order)
        formatted_report = report_to_list(report)
        return formatted_report


class ApiOneDriverResource(Resource):

    @swag_from(API_ONE_DRIVER_SWAGGER_PATH)
    @check_records
    @validate()
    def get(self, query: OrderToValidate, driver_id=None, ):
        order = query.order
        try:
            report = generate_report_from_db(order=order, driver_id=driver_id)
        except DriverNotFound:
            abort(400, f"'{driver_id}' driver id was not found.")
        return report_to_list(report)
