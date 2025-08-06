#  My TikTok Stats – Full Stack App

A full-stack web application that collects and displays TikTok user data and video statistics.

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React.js
- **Database**: PostgreSQL (via Docker)
- **Deployment**: Docker Compose (multi-container)

---

##  Live Endpoints

| Service   | URL                      |
|-----------|--------------------------|
| Frontend  | `http://localhost:5173`  |
| Backend   | `http://localhost:8001`  |
| Docs      | `http://localhost:8001/docs` |
| Database  | `localhost:5434` (via container) |

---

## Docker Setup (Recommended)

> Requires Docker and Docker Compose installed on your machine.

### 1. Create `.env` file inside `backend/`:

```env
# backend/.env

DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/tiktok_project_db
MS_TOKEN=your_token_here # get your own MS_TOKEN from your cookies on tiktok.com

````
### 2. Run the app:
``` docker-compose up --build ```

This will start:

- FastAPI backend at http://localhost:8001

- React frontend at http://localhost:5173

- PostgreSQL at port 5434 locally

## Manual Setup (without Docker)

### Create `.env` file inside `backend/`:

```env
# backend/.env

DATABASE_URL=sqlite:///./tiktok_data.db # You can use any database supported by SQLAlchemy (PostgreSQL, MySQL, SQLite...), just update the DATABASE_URL with the correct connection string for your chosen database.
MS_TOKEN=your_token_here  # get your own MS_TOKEN from your cookies on tiktok.com

````
### Backend
```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

```
### Frontend
```
cd frontend
npm install
npm run dev
```
