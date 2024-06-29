from flask import Flask
from flask_restful import Api
from app.urls import add_urls
from flasgger import Swagger
from app.config import SECRET_KEY
from app.config import TEMPLATES_PATH


def create_app():
    app = Flask(__name__, template_folder=TEMPLATES_PATH)
    app.config['SECRET_KEY'] = SECRET_KEY
    return app


def create_api(app):
    api = Api(app)
    return api


if __name__ == '__main__':
    app = create_app()
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Monaco Racing Report 2018",
            "description": "Monaco Racing Report 2018",
            "version": "0.0.1"
        },
        "schemes": ["http", "https"]
    }
    swagger = Swagger(app, template=template)
    api = create_api(app)
    add_urls(api)
    app.run(debug=True)
