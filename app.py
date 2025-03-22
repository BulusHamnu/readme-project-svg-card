#flask app 
from flask import Flask, render_template, jsonify, url_for
from flask_restful import Api, abort, reqparse
from resource import Singlerepo, Repos
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)

#defining routes
@app.route("/")
@app.route("/home")
def home() :
    return render_template("index.html", title = "Home page | Svg project card")

@app.route("/api/repos")
def missing_username() :
    return jsonify({ "message" : "missing username value, please use: /api/<username>/repos" }), 400


api.add_resource(Repos, "/api/<username>/repos")
api.add_resource(Singlerepo, "/api/<username>/repos/<name>" ) 


@app.errorhandler(404)
def error_404(error) :
    return render_template("error-page.html", title = "Error Page | Svg project card")


if __name__ == "__main__" :
    app.run(debug=True)