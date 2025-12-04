from app.config import SessionLocal
from app.models import User
from app.repository.users_repo import UserRepository
from app.service.transactions import run_in_transaction


class UserService:
    def __init__(self, user_repo:UserRepository):
        self.repository = user_repo

    @run_in_transaction(SessionLocal)
    def create_user(self, user: User, session):
        self.repository.create_user(session, user)

    @run_in_transaction(SessionLocal)
    def get_user_by_id(self, login: str, session):
        user = self.repository.get_user_by_id(session, login)
        return user
