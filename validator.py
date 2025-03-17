from marshmallow import Schema, fields, validate
from functions import themes_colors

#mershmellow
class ReposValidator(Schema) :
    theme = fields.Str(required = True ,validate= validate.OneOf( choices= list(themes_colors.keys())), error= "Invalid color", metadata = {
        "error_message" : {
            "required" : "Missing theme specification"
        }
        })

    pinned = fields.Str(required = True, metadata = {
        "error_message" : {
            "required" : "Please specify False if you want all user's repos, True if you want user's pinned repos."
        }
        })


class RepoValidator(Schema) :
    imageurl = fields.Url(required = False, metadata= { 
        "error_message" : {
            "invalid" : "Must be a valid URL."
        }
        })

    theme = fields.Str(required = True ,validate= validate.OneOf( choices= list(themes_colors.keys())), error= "Invalid color", metadata = {
        "error_message" : {
            "required" : "Missing theme specification"
        }
        })

    