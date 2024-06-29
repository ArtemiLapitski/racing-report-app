import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

SECRET_KEY: str = os.environ.get('SECRET')

TEMPLATES_PATH = Path.cwd()/'app'/'templates'/'templates'

DATETIME_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'

DATABASE_FOLDER = 'db'

DATABASE_FILE = 'data.db'

UNDERLINE = '_' * 79

NUMBER_OF_RACERS_BEFORE_UNDERLINE = 10

SWAGGER_FOLDER = Path(os.path.dirname(os.path.realpath(__file__)))/'swagger'

API_ADD_DRIVER_SWAGGER_PATH = Path(SWAGGER_FOLDER)/"api_create_driver.yml"

API_REPORT_SWAGGER_PATH = Path(SWAGGER_FOLDER)/"api_report.yml"

API_ONE_DRIVER_SWAGGER_PATH = Path(SWAGGER_FOLDER)/"api_one_driver.yml"

REPORT_SWAGGER_PATH = Path(SWAGGER_FOLDER)/"report.yml"

DRIVERS_SWAGGER_PATH = Path(SWAGGER_FOLDER)/"drivers.yml"

ONE_DRIVER_SWAGGER_PATH = Path(SWAGGER_FOLDER)/"one_driver.yml"
