from starlette.requests import Request
from starlette.templating import Jinja2Templates

from app.domain import Cart
from app.repository.item_repo import ItemRepository
from app.repository.order_repo import OrderRepository
from app.repository.users_repo import UserRepository
from app.service.item_service import ItemService
from app.service.order_service import OrderService
from app.service.user_service import UserService


def get_cart(request:Request) -> Cart:
    cart = request.session.get('cart', None)
    if not cart:
        cart = Cart()
        request.session['cart'] = cart
    return cart

jinja_templates = Jinja2Templates(directory="templates")
def templates():
    return jinja_templates

obj_user_service = UserService(UserRepository())
obj_item_service = ItemService(ItemRepository())
obj_order_service = OrderService(OrderRepository())

def user_service():
    return obj_user_service

def item_service():
    return obj_item_service

def order_service():
    return obj_order_service
