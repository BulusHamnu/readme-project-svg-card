#flask app 
from flask import Flask, render_template, jsonify, url_for, request
from flask_restful import Api, abort, reqparse
from api.resource import SingleRepo, Repos
from flask_cors import CORS
from api import logger, FLASK_DEBUG
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
api = Api(app)
# Override flask restfull error handler
api.handle_error = lambda e: app.handle_user_exception(e)
CORS(app)

#defining routes
@app.route("/")
def home() :
    return "<h1>Hello world</h1>", 200

api.add_resource(Repos, "/api/<username>/repos")
api.add_resource(SingleRepo, "/api/<username>/repos/<name>" ) 


# error handlers
@app.errorhandler(404)
def error_404(error):
    return jsonify({ "status" : False, "message": "Resource not found." }), 404

@app.errorhandler(Exception)
def global_error(error):
    if isinstance(error, HTTPException) :
        return jsonify({
            "status" : False,
            "message": error.description
        }), error.code
    return jsonify({
            "status" : False,
            "message": "An unexpected error occured."
        }), 500


if __name__ == "__main__" :
    app.run(debug=FLASK_DEBUG)