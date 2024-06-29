from app.database import extract_from_db
from flask import render_template
from app.config import NUMBER_OF_RACERS_BEFORE_UNDERLINE, UNDERLINE
from report.exceptions import DriverNotFound


def format_seconds(seconds_float: float) -> str:
    """Formats a float object representing seconds and milliseconds to [N days] [N hours] %H:%-M:%S.%f format"""
    assert isinstance(seconds_float, float), "Input should be in float format."

    milliseconds = str(round(seconds_float - int(seconds_float), 3))[2:]
    milliseconds_with_trailing_zeroes = milliseconds.ljust(3, '0')

    seconds = int(seconds_float)

    secs_in_a_day = 86400
    secs_in_a_hour = 3600
    secs_in_a_min = 60

    days, seconds = divmod(seconds, secs_in_a_day)
    hours, seconds = divmod(seconds, secs_in_a_hour)
    minutes, seconds = divmod(seconds, secs_in_a_min)

    time_fmt = f"{minutes}:{seconds:02d}.{milliseconds_with_trailing_zeroes}"

    if hours > 0:
        suffix_hours = "s" if hours > 1 else ""
        time_fmt = f"{hours} hour{suffix_hours} {time_fmt}"

    if days > 0:
        suffix_days = "s" if days > 1 else ""
        time_fmt = f"{days} day{suffix_days} {time_fmt}"

    return time_fmt


def generate_report_from_db(order: bool = False, driver_name: str = None, driver_id: str = None) -> dict:

    race_results = extract_from_db()
    race_results_sorted = sorted(race_results, key=lambda x: x[3], reverse=order)
    report = {
        (abbr, name): {
              'position': position,
              'car': car,
              'result': format_seconds(result)
              }
        for position, (abbr, name, car, result) in enumerate(race_results_sorted, start=1)
    }

    if driver_name:
        report = {(abbr, name): report[(abbr, name)] for abbr, name in report if driver_name == name}
        if not report:
            raise DriverNotFound(driver=driver_name)

    if driver_id:
        report = {(abbr, name): report[(abbr, name)] for abbr, name in report if driver_id == abbr}
        if not report:
            raise DriverNotFound(driver=driver_id)

    return report


def report_to_list(report: dict) -> list:
    report_list = [
        {
            "position": data["position"],
            'abbr': abbr,
            'name': name,
            "car": data["car"],
            "result": data["result"]
        }
        for (abbr, name), data in report.items()
    ]
    return report_list


def report_to_html(report: dict, drivers: bool = False, driver_id: str = None) -> str:
    if drivers:
        if driver_id:
            output = render_template('driver_stat.html', report=report)
        else:
            output = render_template('drivers.html', report=report)
    else:
        report_list = list(report.items())
        output = render_template('report.html',
                                 report_list=report_list,
                                 number_of_results=len(report_list),
                                 underline=UNDERLINE,
                                 number_of_racers_before_underline=NUMBER_OF_RACERS_BEFORE_UNDERLINE
                                 )
    return output
