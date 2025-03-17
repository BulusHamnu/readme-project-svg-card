from flask_restful import Resource, abort
from flask import request
from validator import  ReposValidator, RepoValidator
from marshmallow import ValidationError

repos_validator = ReposValidator()
repo_validator = RepoValidator()

#http://127.0.0.1:5000/api/BulusHamnu/repos?pinned=True&theme=dark&imageurl=hehe
class Repos(Resource) :
    def get(self,username) :
        if len(username) <= 3 :
            abort(400, message = "please provide a valid username!")


        try :
            args = repos_validator.load(request.args)

            pinned_repo = eval(args.get("pinned"))
            theme = args.get("theme")
            imageurl = args.get("imageurl") if args.get("imageurl") else None
            print(pinned_repo,theme,imageurl)

        except ValidationError as error:
            abort(400, message = error.messages )


        return f"This are your repos! {username}", 200


#http://127.0.0.1:5000/api/bulushamnu/repos/svg-card?theme=dark&imageurl=hehe
class Singlerepo(Resource) :
    def get(self,username,name) :
        if len(username) <= 3 :
            abort(400, message = "please provide a valid username!")

        try :
            args = repo_validator.load(request.args)

            theme = args.get("theme")
            imageurl = args.get("imageurl") if args.get("imageurl") else None
            print(name,theme,imageurl)

        except ValidationError as error:
            abort(400, message = error.messages )

        return f"This is your repo! {username}: {name}", 200