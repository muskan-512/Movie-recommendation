from flask import request, jsonify
from routes import user_bp
from app import db
from models.user import User
from models.watched import Watched
from werkzeug.security import generate_password_hash

@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400

    # Hash password
    hashed_password = generate_password_hash(password)

    user = User(username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created", "user_id": user.id}), 201
@user_bp.route("/watched", methods=["POST"])
def add_watched_movie():
    data = request.get_json()

    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    rating = data.get("rating", None)

    if not user_id or not movie_id:
        return jsonify({"error": "Missing required fields"}), 400

    # Validate user
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate movie
    from models.movie import Movie
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    # Add to watched table
    entry = Watched(user_id=user_id, movie_id=movie_id, rating=rating)
    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Movie added to watched list"}), 200
