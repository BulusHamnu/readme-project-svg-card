#flask app 
from flask import Flask, render_template, jsonify, url_for, request
from flask_restful import Api, abort, reqparse
from api.resource import Singlerepo, Repos
from flask_cors import CORS
from api import logger, FLASK_DEBUG


app = Flask(__name__)
api = Api(app)
CORS(app)

#defining routes
@app.route("/")
def home() :
    return "<h1>Hello world</h1>", 200

api.add_resource(Repos, "/api/<username>/repos")
api.add_resource(Singlerepo, "/api/<username>/repos/<name>" ) 


# error handlers
@app.errorhandler(404)
def error_404(error):
    logger.error("User tried to access undefined route: %s", request.path)
    return jsonify({ "status" : False,
    "message": f"404 Not Found: {request.path} cannot be accessed." }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status" : False,
        "message": "An unexpected error occurred."
    }), 500


if __name__ == "__main__" :
    app.run(debug=FLASK_DEBUG)