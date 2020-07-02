import os

from flask_lambda import FlaskLambda
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = FlaskLambda(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    year = db.Column(db.String(50))
    age = db.Column(db.String(10))
    imbd = db.Column(db.String(10))
    rotten_tomatoes = db.Column(db.String(10))
    netflix = db.Column(db.String(10))
    hulu = db.Column(db.String(10))
    prime_video = db.Column(db.String(10))
    disney_plus = db.Column(db.String(10))
    movie_type = db.Column(db.String(10))
    directors = db.Column(db.String(500))
    genres = db.Column(db.String(300))
    country = db.Column(db.String(300))
    language = db.Column(db.String(300))
    runtime= db.Column(db.String(10))

    def __init__(self, title, year, age):
        self.title = title
        self.year = year
        self.age = age


class MovieSchema(ma.Schema):
    class Meta:
        fields = (
            'title',
            'year',
            'age',
            'runtime'
        )



movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route("/hello")
def index():
    
    return jsonify({"message": "Hello, world!"})


@app.route("/movie/list", methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)
    return jsonify(result)
