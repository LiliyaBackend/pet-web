from app.models import User


class UserRepository:
    def create_user(self, session, user:User):
        session.add(user)

    def get_user_by_id(self, session, login:str):
        result = session.query(User).filter_by(login = login).first()
        return result
