from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
import models
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="templates")


@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})


@router.post("/signup", response_class=HTMLResponse)
def signup(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return templates.TemplateResponse(
            "signup.html", {"request": request, "error": "Email already registered."}
        )

    is_first_user = db.query(models.User).count() == 0
    new_user = models.User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
        role="admin" if is_first_user else "user",
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid email or password."}
        )

    token = create_access_token({"sub": user.email})
    redirect_to = "/admin/dashboard" if user.role == "admin" else "/products"
    response = RedirectResponse(url=redirect_to, status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=60 * 60 * 24)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response
