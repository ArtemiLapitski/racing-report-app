from app.templates import HomeResource, ReportResource, DriversResource, OneDriverResource, CreateDriverResource, \
    AddDriverResource
from app.api import ApiAddDriverResource, ApiReportResource, ApiOneDriverResource


def add_urls(api):
    api.add_resource(HomeResource, '/')
    api.add_resource(CreateDriverResource, '/create_driver')
    api.add_resource(AddDriverResource, '/add_driver')
    api.add_resource(ReportResource, '/report')
    api.add_resource(DriversResource, '/report/drivers')
    api.add_resource(OneDriverResource, '/report/drivers/<driver_id>')
    api.add_resource(ApiAddDriverResource, '/api/driver')
    api.add_resource(ApiReportResource, '/api/report')
    api.add_resource(ApiOneDriverResource, '/api/report/drivers/<driver_id>')

