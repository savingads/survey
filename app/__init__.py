import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder="static")
    bootstrap = Bootstrap5(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # the index page
    @app.route("/")
    def index():
        return "Index Page!"

    # template filter for datetime

    @app.template_filter("datetime")
    def format_datetime(value, format="%Y-%m-%d %H:%M"):
        # convert 20120512093436 to datetime object
        value = datetime.strptime(value, "%Y%m%d%H%M%S")
        return value.strftime(format)

    @app.route("/screenshots/<path:path>")
    def screenshots(path):
        # a list of the directory contents of the screenshot folder
        # screenshot_dir = os.listdir("app/static/screenshots")

        # a list of the directory contents of the screenshot folder plus path
        screenshot_dir = os.listdir("app/static/screenshots/" + path)
        # paginate the list
        screenshot_dir = os.listdir("app/static/screenshots/" + path)[0:20]
        return render_template("screenshot_list.html", screenshot_dir=screenshot_dir)
        # return app.send_static_file("screenshots/" + path)

    @app.route("/screenshots/<path:path>/list")
    def screenshot_list(path):
        # a list of the directory contents of the screenshot folder
        screenshot_dir = os.listdir("app/static/screenshots/" + path)[0:20]
        return render_template("screenshot_display.html", screenshot_dir=screenshot_dir)

    @app.route("/screenshots/<path:path>/display/<filename>")
    def screenshot_display(path, filename):
        screenshot_dir = os.listdir("app/static/screenshots/" + path)[0:20]

        selected_screenshot = filename
        return render_template(
            "screenshot_display.html",
            path=path,
            selected_screenshot=selected_screenshot,
            screenshot_dir=screenshot_dir,
        )

    return app
