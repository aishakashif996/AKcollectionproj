from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import engine, Base
from routers import auth_router, products_router, admin_router

# Create all database tables on startup (akcollection.db is auto-generated)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AKcollection")

# Serve product images, QR code, and CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routers
app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(admin_router.router)


@app.get("/")
def root():
    return RedirectResponse(url="/login")
