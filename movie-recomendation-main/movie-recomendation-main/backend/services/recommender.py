
def get_user_preferences(user_id):
    from models.watched import Watched
    from models.movie import Movie

    # get movies user has watched
    watched = Watched.query.filter_by(user_id=user_id).all()
    movie_ids = [w.movie_id for w in watched]

    if not movie_ids:
        return {"genres": {}, "actors": {}}

    # fetch all movie objects
    movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()

    genre_count = {}
    actor_count = {}

    for movie in movies:
        for genre in movie.genres:
            genre_count[genre.id] = genre_count.get(genre.id, 0) + 1
        for actor in movie.actors:
            actor_count[actor.id] = actor_count.get(actor.id, 0) + 1

    return {
        "genres": genre_count,
        "actors": actor_count
    }
def get_candidate_movies(user_id):
    # TODO: fetch movies user has NOT watched
    from models.watched import Watched
    from models.movie import Movie
    watched =Watched.query.filter_by(user_id=user_id).all()
    movie_ids=[w.movie_id for w in watched]
    if not movie_ids:
        return Movie.query.all()
    candidates=Movie.query.filter(Movie.id.notin_(movie_ids)).all()
    return candidates


def compute_similarity(user_prefs, movie):
    genre_score = 0
    for genre in movie.genres:
        genre_score += user_prefs["genres"].get(genre.id, 0)
    actor_score = 0
    for actor in movie.actors:
        actor_score += user_prefs["actors"].get(actor.id, 0)
    rating_score = float(movie.imdb_rating or 0)
    recency_score = 1 if movie.release_year and movie.release_year >= 2020 else 0
    final_score = (genre_score * 0.4) + (actor_score * 0.4) + (rating_score * 0.1) + (recency_score * 0.1)
    return final_score


def recommend_movies(user_id, top_n=10):
    user_prefs=get_user_preferences(user_id)
    candidates=get_candidate_movies(user_id)
    scored_movies=[]
    for movie in candidates:
        score=compute_similarity(user_prefs,movie)
        scored_movies.append((movie,score))
    scored_movies.sort(key=lambda x: x[1],reverse=True)
    top_movies=[movie for movie,score in scored_movies[:top_n]]
    return top_movies
