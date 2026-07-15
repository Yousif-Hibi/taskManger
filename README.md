# Task Manager

Task Manager is a robust FastAPI-based backend application designed for team task management. It provides a comprehensive API for handling users (authentication), projects, and tasks.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (with `asyncpg`)
- **ORM & Migrations:** SQLAlchemy, SQLModel, Alembic
- **Caching & Background Tasks:** Redis
- **Authentication:** JWT (JSON Web Tokens), `bcrypt`
- **Python Version:** 3.10+ (Recommended)

## Project Structure

- `backend/app/`: Contains the main application logic.
  - `auth/`: Authentication and user management.
  - `projects/`: Project management endpoints.
  - `tasks/`: Task management endpoints.
- `backend/migrations/`: Alembic database migration scripts.
- `backend/alembic.ini`: Configuration for Alembic migrations.
- `backend/tests/`: Automated tests.

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Redis server

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Ensure you configure the `.env` file in the `backend/` directory with the necessary database and Redis connection details (e.g., PostgreSQL credentials, Redis URL, JWT secret keys).

### Running the Services

1. **Start Redis Server:**
   ```bash
   redis-server
   ```

2. **Start PostgreSQL Database:**
   Ensure your local PostgreSQL server is running and the database `taskmanager_db` is created. You can connect using:
   ```bash
   psql -U sandov -d taskmanager_db -h localhost -p 5432
   ```

3. **Run Database Migrations:**
   From the `backend` directory, apply the latest migrations to initialize your database schema:
   ```bash
   alembic upgrade head
   ```

4. **Start the FastAPI Application:**
   Run the development server using `uvicorn`:
   ```bash
   uvicorn app.main:app --reload
   ```

   The application will be available at `http://127.0.0.1:8000`.
   You can explore the interactive Swagger API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints Overview

- **Auth:** `/api/auth` (User registration, login, token refresh)
- **Projects:** `/api/project` (CRUD operations for projects)
- **Tasks:** `/api/task` (CRUD operations for tasks)
