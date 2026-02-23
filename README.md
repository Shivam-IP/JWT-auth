# JWT-authentication App
A secure, modern authentication API built with **FastAPI**, **PostgreSQL** (AWS RDS), **JWT**, and best practices.

## Features
- User registration (`/api/v1/auth/register`)
- Login with JWT token (`/api/v1/auth/login`)
- Protected routes (e.g., `/api/v1/auth/me`)
- Password hashing with bcrypt
- Environment variables via `.env`
- Modular structure (routers, models, schemas, core)

## Tech Stack
- **FastAPI** – High-performance API framework
- **SQLAlchemy** – ORM for PostgreSQL
- **Pydantic** (v2) – Data validation & settings
- **python-jose** – JWT handling
- **passlib[bcrypt]** – Secure password hashing
- **PostgreSQL** on AWS RDS
- **Uvicorn** – ASGI server

## Project Structure
   ```bash
   fastapi-auth-project/
   ├── app/
   │   ├── core/          # config, database, security
   │   ├── api/
   │   │   └── v1/        # API routers (auth)
   │   ├── models/        # SQLAlchemy models
   │   └── schemas/       # Pydantic schemas
   ├── .env               # Secrets (gitignore'd)
   ├── requirements.txt
   └── README.md
   ```

## Setup & Run Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/fastapi-auth-project.git
   cd fastapi-auth-project
   ```

2. Create & activate virtual environment:Bash 
    ```bash 
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash 
    Install dependencies:Bashpip install -r requirements.txt
    ```

4. Create .env file (copy from .env.example if exists) and fill:
    ```bash 
    textDATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
    SECRET_KEY=your_random_64_hex_key
    ```

5. Run the server: 
    ```bash 
    uvicorn app.main:app --reload
    ```
    
6. Open docs: http://127.0.0.1:8000/docs

## Deployment (AWS EC2)

- Push code to GitHub
- SSH to EC2 → git clone → venv setup → pip install
- Use systemd service for production (see docs)
- Nginx reverse proxy for port 80/HTTPS
