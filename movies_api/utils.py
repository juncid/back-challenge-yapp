def initialize_movie(movie, data):
        movie.title = data['title']
        movie.year = data['year']
        movie.age = data['age']
        movie.imbd = data['imbd']
        movie.rotten_tomatoes = data['rotten_tomatoes']
        movie.netflix = data['netflix']
        movie.hulu = data['hulu']
        movie.prime_video = data['prime_video']
        movie.disney_plus = data['disney_plus']
        movie.movie_type = data['movie_type']
        movie.directors = data['directors']
        movie.genres = data['genres']
        movie.country = data['country']
        movie.language = data['language']
        movie.runtime = data['runtime']

        return movie