# AKcollection — FastAPI Final Project

A full-stack Python web application built with **FastAPI**, **SQLAlchemy (SQLite)**, and **Jinja2**, for the online handbag brand **AKcollection** (astore.pk / akcollection996).

## Features

- User Signup & Login (JWT-based authentication, stored in secure HTTP-only cookie)
- Password hashing with bcrypt
- Role-based access: regular **User** vs **Admin**
  - The very first account created automatically becomes Admin
- Product catalog page with image, name, description, price, and category
- "Order on WhatsApp" button on every product — opens a pre-filled WhatsApp chat
- Admin dashboard to add and delete products (with image upload)
- Social footer with Instagram, Facebook, WhatsApp links, and a scannable WhatsApp Channel QR code
- SQLite database (`akcollection.db`) — created automatically, no setup required

## Tech Stack

- Python 3
- FastAPI + Uvicorn (ASGI server)
- SQLAlchemy ORM + SQLite
- Jinja2 templates (HTML rendering)
- Passlib (bcrypt password hashing)
- python-jose (JWT tokens)

## How to Run

1. **Extract the ZIP file** and open a terminal inside the `akcollection` folder.

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate it:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Run the server:**
   ```
   uvicorn main:app --reload
   ```

6. **Open your browser and go to:**
   ```
   http://127.0.0.1:8000
   ```

You'll land on the login page. Click **Sign Up** to create an account (the first account you create becomes the Admin automatically). Log in as admin to add products, or create a second normal user account to browse the catalog and use the "Order on WhatsApp" button.

## Project Structure

```
akcollection/
├── main.py                    # FastAPI app entry point
├── database.py                 # SQLAlchemy engine & session
├── models.py                   # User & Product database models
├── schemas.py                  # Pydantic schemas
├── auth.py                     # Password hashing & JWT auth logic
├── routers/
│   ├── auth_router.py          # Signup / Login / Logout routes
│   ├── products_router.py      # Product catalog route
│   └── admin_router.py         # Admin dashboard & product management
├── templates/                  # Jinja2 HTML templates
│   ├── signup.html
│   ├── login.html
│   ├── products.html
│   └── admin_dashboard.html
├── static/
│   ├── css/style.css           # Styling
│   ├── assets/                 # Uploaded product images
│   └── qr/whatsapp_qr.png      # WhatsApp channel QR code
└── requirements.txt
```

## Notes

- The database file `akcollection.db` is generated automatically the first time you run the app — no manual database setup needed.
- All product images uploaded via the admin panel are stored in `static/assets/`.

## Deploying Live (Render)

This repo includes a `render.yaml` so it deploys automatically:

1. Push this project to a GitHub repository.
2. Go to [render.com](https://render.com) and sign up (free) using your GitHub account.
3. Click **New +** → **Blueprint**, and select this repository.
4. Render reads `render.yaml` automatically and sets everything up (build command, start command, and a random `SECRET_KEY`).
5. Click **Apply** / **Deploy**. Wait 2-3 minutes for the build to finish.
6. You'll get a live URL like `https://akcollection.onrender.com` — this is your permanent order/catalog link.

**Note:** On Render's free tier, the SQLite database resets whenever the app redeploys or goes idle and restarts. This is fine for course submission and demos. If you want products/users to persist permanently for real business use, upgrade to a paid Render disk, or ask for help switching to a hosted database later.
