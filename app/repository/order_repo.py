from app.models import Order


class OrderRepository:

    def create_order(self, session, order: Order):
        session.add(order)
        session.flush()
