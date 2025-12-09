from app import db
class Watched(db.Model):
    __tablename__ = "watched"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), primary_key=True)
    watched_at = db.Column(db.DateTime, server_default=db.func.now())
    rating = db.Column(db.Integer)
