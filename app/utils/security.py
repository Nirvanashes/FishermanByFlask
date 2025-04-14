from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import cache, db, login_manager
from app.schema import User
from config import Config


@login_manager.user_loader
def load_user(user_id):
    # if "user_id" in session and str(session["user_id"]) == str(user_id):
    #     return None
    # cache_key = f"user_{user_id}"
    # user = cache.get(cache_key)
    # if user is None:
    #     user = db.session.get(User, user_id)
    #     if user:
    #         cache.set(cache_key, user, timeout=3600)
    return db.get_or_404(User, user_id)


def generate_password(password: str) -> str:
    return generate_password_hash(
        password=password,
        method=Config.PASSWORD_HASH_METHOD,
        salt_length=16
    )


def check_password(password_hash, password):
    return check_password_hash(
        pwhash=password_hash,
        password=password
    )
