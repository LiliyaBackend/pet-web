import json
from datetime import datetime

import stomp

from app.config import sql_engine, SessionLocal
from app.domain import CartItem
from app.models import Order, OrderItem
from app.repository.order_repo import OrderRepository
from app.service.transactions import run_in_transaction


class OrderService:
    def __init__(self, repository:OrderRepository):
        self.repository = repository

    def create_order_item(self, cart_item: CartItem, order: Order):
        return OrderItem(
            order=order,
            item=cart_item['operation'],
            count=1,
            price=0
        )

    @run_in_transaction(SessionLocal)
    def create_order(self, order: Order, cart_items: list, session):
        current_timestamp = datetime.now()
        order.created = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        order.items = [self.create_order_item(item, order) for item in cart_items]

        self.repository.create_order(session, order)
        self.send_order(order)

    def send_order(self, order: Order):
        # The auto_content_length parameter should be set to False to send Text message instead of Binary
        conn = stomp.Connection([("localhost", 61613)], auto_content_length=False)
        conn.connect('admin', 'admin', wait=True)
        try:
            message = {
                "orderId": order.order_number,
                "total": order.get_total(),
                "userId": order.userId
            }
            msg_body = json.dumps(message)
            conn.send(destination="shop06.orders.for.approve.json", body=msg_body)
        finally:
            conn.disconnect()
