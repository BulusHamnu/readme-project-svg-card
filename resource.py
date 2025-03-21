from flask_restful import Resource, abort
from flask import request, Response
from validator import  ReposValidator, RepoValidator
from marshmallow import ValidationError
import asyncio
from functions import get_repos, get_repo, themes_colors

repos_validator = ReposValidator()
repo_validator = RepoValidator()

class Repos(Resource) :
    def get(self,username) :
        if len(username) <= 3 :
            abort(400, message = "please provide a valid username!")


        try :
            args = repos_validator.load(request.args)

            pinned_repo = eval(args.get("pinned"))
            theme = args.get("theme") 

            svg_results = asyncio.run(get_repos(username,pinned_repo,theme, None))
            return svg_results[0] , svg_results[1]

        except ValidationError as error:
            abort(400, message = error.messages )



class Singlerepo(Resource) :
    def get(self,username,name) :
        if len(username) <= 3 :
            abort(400, message = "please provide a valid username!")

        try :
            args = repo_validator.load(request.args)

            theme = args.get("theme")
            imageurl = args.get("imageurl") if args.get("imageurl") else None
            svg_content = asyncio.run(get_repo(username, name, theme, imageurl))

            return Response(svg_content[0], content_type="image/svg+xml", status = svg_content[1])

        except ValidationError as error:
            abort(400, message = error.messages )

        