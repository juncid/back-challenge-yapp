from marshmallow import Schema, fields

class MovieSchema(Schema):
    id = fields.Integer(required=False)
    title = fields.String(required=True)
    year = fields.String(required=True)
    age = fields.String(required=True)
    imbd = fields.String(required=True)
    rotten_tomatoes = fields.String(required=True)
    netflix = fields.String(required=True)
    hulu = fields.String(required=True)
    prime_video = fields.String(required=True)
    disney_plus = fields.String(required=True)
    movie_type = fields.String(required=True)
    directors = fields.String(required=True)
    genres = fields.String(required=True)
    country = fields.String(required=True)
    language = fields.String(required=True)
    runtime= fields.String(required=True)