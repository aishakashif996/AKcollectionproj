from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
import models
from auth import get_current_user

router = APIRouter(tags=["products"])
templates = Jinja2Templates(directory="templates")

# ---- Social / contact links (AKcollection) ----
SOCIAL_LINKS = {
    "whatsapp_number": "923310280975",
    "instagram": "https://www.instagram.com/akcollection996",
    "facebook": "https://www.facebook.com/share/1dJKZZwyyG/",
    "qr_code": "/static/qr/whatsapp_qr.png",
    "brand_name": "AKcollection",
}


@router.get("/products", response_class=HTMLResponse)
def products_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    products = db.query(models.Product).all()
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "user": user,
            "products": products,
            "social": SOCIAL_LINKS,
        },
    )
