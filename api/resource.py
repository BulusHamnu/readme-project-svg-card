from flask_restful import Resource, abort
from flask import request, Response, jsonify
from .validator import  ReposValidator, RepoValidator, ReposJsonValidator
from marshmallow import ValidationError
import asyncio
from .functions import get_repos, get_repo, themes_colors, get_selected_repos
from . import logger , AppError

repos_validator = ReposValidator()
repo_validator = RepoValidator()
repos_json_validator = ReposJsonValidator()

def validate_username(username):
    if len(username) <= 3 :
        raise AppError(400, "Please provide a valid username.")

class Repos(Resource) :
    def get(self,username) :
        validate_username(username)
        try :
            logger.info("Getting all repositories for: %s", username)

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
                raise AppError(500, "An unexpected error occured.")

            return { "status": True, "message": "Repositories retrived successfully.", 'data' : svg_results.get("data") } , 200

        except ValidationError as error:
            raise AppError(400, error.messages )

    def post(self,username) :
        validate_username(username)
        try :
            logger.info("Getting all repos for: %s", username)
            json_data = repos_json_validator.load(request.json)
            repos = json_data.get("repos")
            svg_list_result = asyncio.run(get_selected_repos(username,repos))

            if not svg_list_result.get("status") :
                logger.error("An error occured while getting repos for: %s - %s", username, svg_list_result.get("error") or "Repos not found." ) 

                raise AppError(404, f"No Repos with these names were found: { str([repo.get('name') for repo in repos]) }")
            
            return { "status": True, "message": "Repositories retrived successfully.", "data": svg_list_result.get("data") } , 200
        except ValidationError as error :
            return { "status" : False, "message" : error.messages }, 400


class SingleRepo(Resource) :
    def get(self,username,name) :
        validate_username(username)
        try :
            logger.info("Getting  %s repo for: %s",username, name)
            args = repo_validator.load(request.args)

            theme = args.get("theme")
            imageurl = args.get("imageurl") if args.get("imageurl") else None
            svg_result = asyncio.run(get_repo(username, name, theme, imageurl))
            # check for error
            if not svg_result.get("status") :
                logger.error("An error occured while getting repo for: %s - %s", username, "Repo not found.") 
                raise AppError(404, "Repo Not Found")

            return Response(svg_result.get("data"), content_type="image/svg+xml", status = 200 )

        except ValidationError as error:
            raise AppError(400, error.messages )

        