from app.models import MathItem


class ItemRepository:
    def get_formulas(self, session):
        result = session.query(MathItem).all()
        return result

    def get_formula_by_id(self, session, id):
        result = session.get(MathItem, id)
        return result
