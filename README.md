## Web framework: Flask restful api
Application with web interface and API service for storing data on drivers and displaying results of the race. 
Peewee ORM along with SQLite database are used for this project. Validation of inputs from web is done via WTForms, API - Pydantic.


## Installation:
Clone the project:
```
git clone https://github.com/ArtemiLapitski/racing-report-app.git
```
Move to project directory:
```
cd racing-report-app
```

Create a virtualenv or skip this point.

Activate virtualenv.

Install the requirements:

```
pip install -r requirements.txt
```

Create the file .env with virtual environments (see in .env.example).

Run the following in root project folder to create database:
```
python create_database.py
```
Run server:
```
python main.py
```

Url: http://127.0.0.1:5000 


## Usage:

User can create drivers and display race results both via web interface and API requests. 
Routes may get the `order` parameter which should be `?order=asc` or `?order=desc`. 
If order parameter is `asc` or none, then fastest racer will be at the first position in race result.

### Web:



- http://127.0.0.1:5000/create_driver - create a driver

- http://127.0.0.1:5000/report - show race statistics

- http://127.0.0.1:5000/report/drivers - show a list of driver's names and abbreviations. Abbreviation is a link to info about a driver.

- http://127.0.0.1:5000/report/drivers/ABC  - show info about a driver by abbreviation

### API:

- GET http://127.0.0.1:5000/api/report - show race statistics

Example response:
```
[
  {
    "position": 1,
    "abbr": "SCH",
    "name": "Michael Schumacher",
    "car": "Ferrari",
    "result": "0:00.079"
  },
  {
    "position": 2,
    "abbr": "MAN",
    "name": "Mario Andretti",
    "car": "BMW",
    "result": "1 day 0:00.079"
  }
]
```

- POST http://127.0.0.1:5000/api/driver - create a driver

Example request body:
```
  {
    "abbr": "MSH",
    "name": "Michael Schumacher",
    "car": "Ferrari",
    "start": "2018-05-24_12:04:02.979",
    "end": "2018-05-24_12:08:02.979"
  }
```

- GET http://127.0.0.1:5000/api/report/drivers/MSH - show info about a driver by abbreviation

Example response:
```
[
    {
        "position": 2,
        "abbr": "MSH",
        "name": "Michael Schumacher",
        "car": "FERRARI",
        "result": "4:00.000"
    }
]
```
