# from flask import Flask
#
# from app.extensions import db,init_extensions
# from config import Config
# from app.auth.models import User
#
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     init_extensions(app)
#     with app.app_context():
#         db.create_all()
