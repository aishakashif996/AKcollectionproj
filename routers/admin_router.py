import os
import shutil
import uuid

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
import models
from auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")

ASSETS_DIR = os.path.join("static", "assets")


def admin_guard(request: Request, db: Session):
    """Returns user if admin, else a redirect response."""
    user = get_current_user(request, db)
    if not user:
        return None, RedirectResponse(url="/login", status_code=303)
    if user.role != "admin":
        return None, RedirectResponse(url="/products", status_code=303)
    return user, None


@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    user, redirect = admin_guard(request, db)
    if redirect:
        return redirect

    products = db.query(models.Product).all()
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "user": user, "products": products},
    )


@router.post("/products/add")
def add_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    category: str = Form("General"),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user, redirect = admin_guard(request, db)
    if redirect:
        return redirect

    os.makedirs(ASSETS_DIR, exist_ok=True)
    ext = os.path.splitext(image.filename)[1] or ".jpg"
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(ASSETS_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_product = models.Product(
        name=name,
        description=description,
        price=price,
        category=category,
        image_filename=unique_filename,
    )
    db.add(new_product)
    db.commit()

    return RedirectResponse(url="/admin/dashboard", status_code=303)


@router.post("/products/delete/{product_id}")
def delete_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    user, redirect = admin_guard(request, db)
    if redirect:
        return redirect

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        image_path = os.path.join(ASSETS_DIR, product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        db.delete(product)
        db.commit()

    return RedirectResponse(url="/admin/dashboard", status_code=303)
