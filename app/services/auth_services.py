from app.extensions import db
from app.schema import User
from app.utils.security import generate_password, check_password


class AuthServices:
    @staticmethod
    def get_user_by_id(user_id):
        return db.get_or_404(User, user_id)

    @staticmethod
    def get_user_by_email(email):
        return db.session.execute(db.select(User).where(User.email == email)).scalar()

    @staticmethod
    def create_user(email, name, password):
        hash_and_salted_password = generate_password(password)
        new_user = User(
            email=email,
            name=name,
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
