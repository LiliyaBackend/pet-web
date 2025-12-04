import app.domain
from app.config import SessionLocal
from app.repository.item_repo import ItemRepository
from app.service.transactions import run_in_transaction


class ItemService:
    def __init__(self, repository:ItemRepository):
        self.repository = repository

    @run_in_transaction(SessionLocal)
    def get_formulas(self, session):
        return self.repository.get_formulas(session)

    @run_in_transaction(SessionLocal)
    def get_formula_by_id(self, id, session):
        return self.repository.get_formula_by_id(session, id)
