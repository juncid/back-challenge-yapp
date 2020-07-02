import os

from flask_lambda import FlaskLambda
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from marshmallow import ValidationError

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



class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie



movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route("/hello")
def index():
    
    return jsonify({"message": "Hello, world!"})


@app.route("/movie/list", methods=['GET'])
def get_movies():
    all_movies = Movie.query.order_by(Movie.title).all()
    result = movies_schema.dump(all_movies)
    return jsonify(result)


@app.route("/movie", methods=['POST', 'PUT', 'DELETE'])
def create_update_movie():

    if request.method == 'POST':
        data = request.get_json()

        return jsonify(data)

    elif request.method == 'PUT': 
        data = request.get_json()

        movie_to_update = Movie.query.get(data['id'])

        movie_to_update.title = data['title']
        movie_to_update.year = data['year']
        movie_to_update.age = data['age']
        movie_to_update.imbd = data['imbd']
        movie_to_update.rotten_tomatoes = data['rotten_tomatoes']
        movie_to_update.netflix = data['netflix']
        movie_to_update.hulu = data['hulu']
        movie_to_update.prime_video = data['prime_video']
        movie_to_update.disney_plus = data['disney_plus']
        movie_to_update.movie_type = data['movie_type']
        movie_to_update.directors = data['directors']
        movie_to_update.genres = data['genres']
        movie_to_update.country = data['country']
        movie_to_update.language = data['language']
        movie_to_update.runtime = data['runtime']

        db.session.commit()

        result = movie_schema.dump(movie_to_update)

        return jsonify(result)

    elif request.method == 'DELETE':

        data = request.args.get('id')
        movie = Movie.query.get(data)

        result = movie_schema.dump(movie)

        return jsonify(result)
        
    
