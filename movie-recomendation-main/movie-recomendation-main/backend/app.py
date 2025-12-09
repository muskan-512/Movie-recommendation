from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes import search_bp, recommend_bp, user_bp
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(recommend_bp, url_prefix='/recommend')
    app.register_blueprint(user_bp, url_prefix='/user')
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
