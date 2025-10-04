from flask_restful import Resource, abort
from flask import request, Response, jsonify
from .validator import  ReposValidator, RepoValidator, ReposJsonValidator
from marshmallow import ValidationError
import asyncio
from .functions import get_repos, get_repo, themes_colors, get_selected_repos
from . import logger 

repos_validator = ReposValidator()
repo_validator = RepoValidator()
repos_json_validator = ReposJsonValidator()

class Repos(Resource) :
    def get(self,username) :
        # check for username length
        if len(username) <= 3 :
            return { 
                "status" : False,
                "message" : "Please provide a valid username." 
                }, 400
        logger.info("Getting all repos for: %s", username)

        try :
            args = repos_validator.load(request.args)

            pinned_repo = eval(args.get("pinned").capitalize())
            theme = args.get("theme") 

            # query for repos
            svg_results = asyncio.run(get_repos(
                username,
                pinned_repo,
                theme, None
                ))
            status = svg_results.get("status")

            if not status:
                logger.error("An error occured while getting repos for: %s - %s", username, svg_results.get("error"))
                return { "status": False, "message" : "An unexpected error occured." }, 500

            return { "status": True, "message": "Repos retrive successful.", 'data' : svg_results.get("data") } , 200

        except ValidationError as error:
            abort(400, message = error.messages )

    def post(self,username) :
        if len(username) <= 3 :
            return { "status": False, "message" : "please provide a valid username." }, 400
        logger.info("Getting all repos for: %s", username)

        try :
            json_data = repos_json_validator.load(request.json)
            repos = json_data.get("repos")

            svg_list_result = asyncio.run(get_selected_repos(username,repos))

            if not svg_list_result.get("status") :
                logger.error("An error occured while getting repos for: %s - %s", username, svg_list_result.get("error") or "Repos not found." ) 

                return { "status" : False, "message" : f"No Repos with this names are found { str([repo.get('name') for repo in repos]) }"} , 404
            
            return { "status": True, "data": svg_list_result.get("data") } , 200
        except ValidationError as error :
            return { "status" : False, "message" : error.messages }, 400


class Singlerepo(Resource) :
    def get(self,username,name) :
        if len(username) <= 3 :
            return { "status": False, "message" : "please provide a valid username." }, 400
        logger.info("Getting  %s repo for: %s",name, username)

        try :
            args = repo_validator.load(request.args)

            theme = args.get("theme")
            imageurl = args.get("imageurl") if args.get("imageurl") else None
            svg_result = asyncio.run(get_repo(username, name, theme, imageurl))
            # check for error
            if not svg_result.get("status") :
                logger.error("An error occured while getting repo for: %s - %s", username, "Repos not found.") 
                return { "status": False, "message" : "Repo Not Found" }, 404

            return Response(svg_result.get("data"), content_type="image/svg+xml", status = 200 )

        except ValidationError as error:
            abort(400, message = error.messages )

        