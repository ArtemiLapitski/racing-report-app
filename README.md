Web framework: Flask restful api


Clone a project and move to it:

$ git clone http://git.foxminded.ua/foxstudent103535/task9-convert-and-store-data-to-the-database.git

$ cd task9-convert-and-store-data-to-the-database


Create a virtualenv or skip this point.

Activate virtualenv.

Install the requirements:

$ pip install -r requirements.txt

Create the file .env with virtual environments (see in .env.example):

SECRET_KEY='your_secret_key'

Run 'python create_database.py' while in root project folder.


Run server:

$ set FLASK_APP=main.py

$ flask run


Urls: http://127.0.0.1:5000 
