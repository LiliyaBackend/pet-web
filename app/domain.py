from app.models import MathItem


class CartItem(dict):
    operation: MathItem
    operand: int


class Cart(dict):
    items:list[CartItem] = []

    def add_item(self, item):
        self.items.append(item)



