from marshmallow import Schema, fields, validate, ValidationError
from .functions import themes_colors

#mershmellow
class ReposValidator(Schema) :
    theme = fields.Str(required = True ,validate= validate.OneOf( choices= list(themes_colors.keys())), error= "Invalid color" )
    pinned = fields.Str(required = True)


class RepoValidator(Schema) :
    imageurl = fields.Url(required = False)
    theme = fields.Str(required = True ,validate= validate.OneOf( choices= list(themes_colors.keys())), error= "Invalid theme" )

# check and validate indivitual repo for ReposJsonValidator
class RepoShema(Schema) :
    name = fields.Str(required=True)
    theme = fields.Str(required=True, validate = validate.OneOf( choices= list(themes_colors.keys())), error="Invalid color")
    imageurl = fields.Url(required=False )


class ReposJsonValidator(Schema) :
    repos = fields.List(fields.Nested(RepoShema), required = True, error= "Empty list")

            
    