from flask import Flask
from flask_migrate import Migrate
from .models import db
import os

def create_app():
    # create the flask app
    app = Flask(__name__)
    
    # config from object
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///lateshow.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key-please-change-in-production'
    
    # init extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # register blueprints
    from .routes import api
    app.register_blueprint(api)
    
    # quick health check route
    @app.route('/')
    def index():
        return {"status": "ok", "message": "Late Show API running"}
    
    return app