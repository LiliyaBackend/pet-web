from typing import Annotated

from fastapi import APIRouter, Form, Query, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dependencies import get_cart, templates, item_service, order_service
from app.domain import CartItem
from app.models import OrderItem, Order
from app.service.item_service import ItemService
from app.service.order_service import OrderService

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request,
              item_service: Annotated[ItemService, Depends(item_service)],
              templates = Depends(templates),
              cart = Depends(get_cart)):
    return templates.TemplateResponse("index.html", {"request": request, "items": item_service.get_formulas(),
                                                     "cart": cart})


@router.post("/add_to_cart")
def add_to_cart(request: Request,
                item_service: Annotated[ItemService, Depends(item_service)],
                cart = Depends(get_cart),
                id: Annotated[str, Form()] = None, operand: Annotated[int, Form()] = 0):
    item = item_service.get_formula_by_id(id)
    if not item:
        return HTMLResponse(content="", status_code=400)
    else:
        cart.add_item(CartItem(operation=item, operand=operand))
        return PlainTextResponse(content=str(len(cart.items)))

@router.post("/remove_from_cart")
def remove_from_cart(request: Request,
                     cart = Depends(get_cart),
                     position: Annotated[int, Query()] = -1):
    if position == -1 or position>=len(cart.items):
        return PlainTextResponse(content="Error", status_code=400)

    cart.items.pop(position)
    return RedirectResponse(url="/cart", status_code=302)



@router.get("/cart", response_class=HTMLResponse)
def show_cart(request: Request,
              cart=Depends(get_cart),
              templates = Depends(templates)):
    return templates.TemplateResponse("cart.html", {"request": request, "cart": cart})


@router.get("/payment", response_class=HTMLResponse)
def show_payment(request: Request,
                 cart=Depends(get_cart),
                 templates = Depends(templates)):
    return templates.TemplateResponse("payment.html", {"request": request, "cart": cart})


@router.post("/payment", response_class=HTMLResponse)
def perform_payment(request: Request,
                    templates: Annotated[Jinja2Templates, Depends(templates)],
                    order_service: Annotated[OrderService, Depends(order_service)],
                    cart=Depends(get_cart),
                    addr: Annotated[str, Form()] = None, credit_card: Annotated[str, Form()] = None):
    if not cart.items:
        return PlainTextResponse(content="Error", status_code=400)

    if not addr or not credit_card:
        return PlainTextResponse(content="Error", status_code=400)

    order = Order(
        userId = request.session['login'],
        card = credit_card,
        address = addr,
    )
    order_service.create_order(order, cart.items)
    cart.items.clear()
    return templates.TemplateResponse("order.html", {"request": request, "cart": cart, "order": order})

