from flask import request, redirect, url_for, make_response, render_template
from flask_restful import Resource
from report import DriverNotFound
from flasgger import swag_from
from app.database import create_racer, check_records_in_db
from report import generate_report_from_db, report_to_html
from app.templates.forms import CreateRacerForm
from datetime import datetime
from app.config import REPORT_SWAGGER_PATH, DRIVERS_SWAGGER_PATH, ONE_DRIVER_SWAGGER_PATH, DATETIME_FORMAT


def order_to_bool(order: str) -> bool:
    return True if order == "desc" else False


def check_records(func):
    def wrapper(*args, **kwargs):

        if not check_records_in_db():
            return redirect(url_for('homeresource'))

        return func(*args, **kwargs)
    return wrapper


def string_to_datetime(string: str) -> datetime:
    return datetime.strptime(string, DATETIME_FORMAT)


class HomeResource(Resource):
    def get(self):
        form = CreateRacerForm(meta={'csrf': False})
        return make_response(render_template('home.html', form=form))


class CreateDriverResource(Resource):
    def get(self):
        form = CreateRacerForm(meta={'csrf': False})
        if request.args.get('success', None):
            success_msg = 'Driver has been successfully added!'
            return make_response(render_template('create_driver.html', form=form, success_msg=success_msg))
        else:
            return make_response(render_template('create_driver.html', form=form))


class AddDriverResource(Resource):
    def post(self):

        form = CreateRacerForm(meta={'csrf': False})

        if form.validate_on_submit():

            create_racer(
                form.name.data,
                form.abbr.data,
                form.car.data,
                form.start.data,
                form.end.data
            )

            return redirect(url_for('createdriverresource', success=True))
        else:
            return make_response(render_template('create_driver.html', form=form))


class ReportResource(Resource):

    @swag_from(REPORT_SWAGGER_PATH)
    @check_records
    def get(self):
        order = request.args.get('order', None)

        if order and order not in ('desc', 'asc'):
            return f"'{order}' order argument is invalid. Only 'desc' and 'asc' are allowed."

        order = order_to_bool(order)

        report = generate_report_from_db(order)
        formatted_report = report_to_html(report)

        response = make_response(formatted_report)
        response.content_type = 'text/html'
        return response


class DriversResource(Resource):

    @swag_from(DRIVERS_SWAGGER_PATH)
    @check_records
    def get(self):
        order = request.args.get('order', None)

        if order and order not in ('desc', 'asc'):
            return f"'{order}' order argument is invalid. Only 'desc' and 'asc' are allowed."

        order = order_to_bool(order)

        report = generate_report_from_db(order=order)
        formatted_report = report_to_html(report, drivers=True)

        response = make_response(formatted_report)
        response.content_type = 'text/html'
        return response


class OneDriverResource(Resource):

    @swag_from(ONE_DRIVER_SWAGGER_PATH)
    @check_records
    def get(self, driver_id=None):

        order = request.args.get('order', None)
        if order and order not in ('desc', 'asc'):
            return f"'{order}' order argument is invalid. Only 'desc' and 'asc' are allowed."
        order = order_to_bool(order)

        try:
            report = generate_report_from_db(order=order, driver_id=driver_id)
        except DriverNotFound:
            return f"'{driver_id}' driver id was not found."

        formatted_report = report_to_html(report, drivers=True, driver_id=driver_id)

        response = make_response(formatted_report)
        response.content_type = 'text/html'
        return response
