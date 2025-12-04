from typing import Annotated, Union

from fastapi import APIRouter, Header, Form, Depends
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dependencies import get_cart, templates, user_service
from app.models import User
from app.routers.forms import UserForm
from app.service.user_service import UserService

router = APIRouter()

@router.get("/register", response_class=HTMLResponse)
def start_register(request: Request,
                   templates: Annotated[Jinja2Templates, Depends(templates)],
                   cart = Depends(get_cart)):
    return templates.TemplateResponse("register.html", {"request": request, "cart": cart})


@router.post("/register", response_class=HTMLResponse)
async def perform_register(request: Request,
                           templates: Annotated[Jinja2Templates, Depends(templates)],
                           user_service: Annotated[UserService, Depends(user_service)],
                           cart = Depends(get_cart)
                           ):
    form_data = dict(await request.form())

    try:
        user_form = UserForm(**form_data)
    except ValidationError as exc:
        print(exc)

        error_messages = {error['loc'][0]: error['msg'] for error in exc.errors() if error['loc']}
        if not error_messages:
            error_messages = {'password2': error['msg'] for error in exc.errors() if not error['loc']}

        form_data['password1'] = ''
        form_data['password2'] = ''
        return templates.TemplateResponse("register.html", {"request": request, "cart": cart,
                                                            'errors': error_messages, 'regform': form_data})

    user = User(login=user_form.login, password=user_form.password1, name=user_form.name,
                email=user_form.email, advertising=user_form.advertising is not None)

    user_service.create_user(user)
    return RedirectResponse(url="/", status_code=302)


@router.get("/login", response_class=HTMLResponse)
def start_login(request:Request,
                templates: Annotated[Jinja2Templates, Depends(templates)],
                cart = Depends(get_cart),
                referer: Annotated[Union[str, None], Header()] = None):
    return templates.TemplateResponse("login.html", {"request": request, "cart": cart, "return_url": referer})

@router.post("/login", response_class=HTMLResponse)
def perform_login(request: Request,
                  templates: Annotated[Jinja2Templates, Depends(templates)],
                  user_service: Annotated[UserService, Depends(user_service)],
                  cart=Depends(get_cart),
                  login: Annotated[str, Form()] = None, pwd: Annotated[str, Form()] = None,
                  referer: Annotated[str, Form()] = None):
    if not login or not pwd:
        return templates.TemplateResponse("login.html", {"request": request, "cart": cart, 'error': '1'})
    user = user_service.get_user_by_id(login)
    if user and user.password == pwd:
        request.session['login'] = login
        back_url = referer if referer else "/"
        return RedirectResponse(url=back_url, status_code=302)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "cart": cart, 'error': '1'})


@router.post("/logout", response_class=HTMLResponse)
def perform_logout(request: Request, referer: Annotated[str, Form()] = None):
    request.session.pop('login','')
    back_url = referer if referer else "/"
    return RedirectResponse(url=back_url, status_code=302)
