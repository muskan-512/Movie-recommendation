from routes import recommend_bp
from flask import request, jsonify
from services.recommender import recommend_movies
@recommend_bp.route('/movies/<int:user_id>', methods=['GET'])
def recommend_for_user(user_id):
    movies = recommend_movies(user_id)
    return {"movie":[m.title for m in movies]}
