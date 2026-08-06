from flask import Flask
import os


def create_app():

    app = Flask(__name__, template_folder="../templates")


    from flask_app.app_blueprints.web import quiz
    from flask_app.app_blueprints.result import quiz_results

    app.register_blueprint(quiz)
    app.register_blueprint(quiz_results, url_prefix='/results', name='results')

    return app