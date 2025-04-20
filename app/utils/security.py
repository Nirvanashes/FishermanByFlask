from flask import session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import cache, db, login_manager
from app.schema import User
from config import Config


@login_manager.user_loader
def load_user(user_id):
    # return UserInfo.get(user_id)
    return db.get_or_404(User, user_id)


def generate_password(password: str) -> str:
    return generate_password_hash(
        password=password,
        method=Config.PASSWORD_HASH_METHOD,
        salt_length=4
    )


def check_password(password_hash, password):
    return check_password_hash(
        pwhash=password_hash,
        password=password
    )

# class UserInfo(UserMixin):
#     def __init__(self, user):
#         self.name = user.name
#         self.password_hash = user.password
#         self.email = user.email
#         self.id = user.id
#
#     @staticmethod
#     def get(user_id):
#         if not user_id:
#             return None
#         user = db.get_or_404(User, user_id)
#         if user:
#             return UserInfo(user)
#         return None
# if "user_id" in session and str(session["user_id"]) == str(user_id):
#     return session.get()
# cache_key = f"user_{user_id}"
# user = cache.get(cache_key)
# if user is None:
#     user = db.get_or_404(User, user_id)
#     if user:
#         cache.set(cache_key, user, timeout=3600)
# return user
