from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager



db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app=app)
    from .users.routes import create_authentication_routes
    from .payments.routes import create_payment_routes
    db.init_app(app)
    jwt.init_app(app)
    create_authentication_routes(api=api)
    create_payment_routes(api=api)
    with app.app_context():
        try:
            db.create_all()
        except Exception as error:
            print(error)
        return app
