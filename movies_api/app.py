import os

from flask_lambda import FlaskLambda
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

from serializers import MovieSchema
from utils import initialize_movie


app = FlaskLambda(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['JSON_SORT_KEYS']=False

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



@app.route("/movie/list", methods=['GET'])
def get_movies():
    movies_schema = MovieSchema(many=True)
    all_movies = Movie.query.order_by(Movie.title).all()

    result = movies_schema.dump(all_movies)
    return jsonify(result)


@app.route("/movie", methods=['POST', 'PUT', 'DELETE'])
def create_update_movie():

    movie_schema = MovieSchema()

    if request.method == 'POST':
        data = request.get_json()

        try:
            movie_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 404

        movie = Movie()
        movie = initialize_movie(movie, data)

        db.session.add(movie)
        db.session.commit()

        result = movie_schema.dump(movie)

        return jsonify(result), 201

    elif request.method == 'PUT': 
        data = request.get_json()

        try:
            movie_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 404

        movie_to_update = Movie.query.get_or_404(data['id'])

        if not movie_to_update:
            result = movie_schema.dump(movie_to_update)
            return jsonify(result)

        
        movie = initialize_movie(movie_to_update, data)

        db.session.commit()

        result = movie_schema.dump(movie)

        return jsonify(result), 201

    elif request.method == 'DELETE':

        id_movie = request.args.get('id')
        movie = Movie.query.get_or_404(id_movie)

        db.session.delete(movie)
        db.session.commit()
        
        return jsonify({"message": "Movie Deleted!"}), 202
