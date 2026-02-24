from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models.user import Base, User
from app.core.security import (
    get_current_user,
    create_access_token,
    verify_password,
    get_password_hash
)
from app.schemas.user import UserOut

# Create tables (development only)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JWT Auth API",
    description="JWT + PostgreSQL Authentication",
    version="1.0"
)

# Templates aur Static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Router include (agar alag file mein auth.py hai)
from app.api.v1.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

# ==================== HTML Pages ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/me", response_class=HTMLResponse)
async def me_page(
    request: Request,
    current_user: UserOut = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "me.html",
        {"request": request, "user": current_user}
    )

# ==================== Form Handlers ====================

@app.post("/register-form")
async def handle_register_form(
    request: Request,
    username: str = Form(...),
    email: str | None = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username already taken"}
        )

    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/login", status_code=303)


@app.post("/login-form")
async def handle_login_form(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"}
        )

    access_token = create_access_token(data={"sub": user.username})
    
    response = RedirectResponse(url=f"/me?token={access_token}", status_code=303)
    return response

@app.get("/logout", response_class=HTMLResponse)
async def logout():
    # JWT stateless hai, client se token delete karna padta hai
    return HTMLResponse(content="<h2>Logged out! <a href='/login'>Login again</a></h2>")
