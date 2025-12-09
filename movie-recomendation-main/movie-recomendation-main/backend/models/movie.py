from app import db

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.Integer)
    imdb_rating = db.Column(db.Numeric(3, 1))
    director = db.Column(db.String(255))
    synopsis = db.Column(db.Text)
