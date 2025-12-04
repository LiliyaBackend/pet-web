import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from app.restapi import itemsapi
from app.routers import users, items



app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)
app.include_router(itemsapi.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
