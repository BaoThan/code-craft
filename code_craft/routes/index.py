from flask_cors import cross_origin

from . import routes


@routes.route("/", methods=["HEAD", "GET"])
@cross_origin()
def index():
    return "hello from code-craft"
