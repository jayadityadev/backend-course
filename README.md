# Social Media App (Full-Stack)

A full-stack social media application with FastAPI backend and Next.js frontend, featuring user authentication, post management, and voting functionality.

## Features

- **User Authentication** - JWT-based authentication with secure password hashing
- **Post Management** - Full CRUD operations with ownership-based authorization
- **Voting System** - Upvote/downvote functionality with real-time vote counts
- **Profile Management** - Update email/password, delete account
- **Post Visibility** - Published posts visible to all, unpublished posts visible to owners only
- **Search & Pagination** - Query posts by title with limit/offset pagination

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database with SQLAlchemy ORM
- **JWT** - Token-based authentication
- **Alembic** - Database migrations
- **pwdlib** - Password hashing (Argon2)

### Frontend
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **React 19** - UI library

## Quick Start

### Backend Setup

### 1. Clone the repository
```bash
git clone https://github.com/jayadityadev/social-media-api
cd social-media-api
```

### 2. Set up Python environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

cd backend
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the `backend/` directory:

```env
# Database Configuration
DB_USERNAME=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOSTNAME=localhost
DB_PORT=5432
DB_NAME=social_media_db

# JWT Configuration
JWT_SECRET_KEY=your_secret_key_here  # Generate with: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRE_TIME=30  # Token expiry in minutes
```

### 4. Set up PostgreSQL database
Ensure PostgreSQL is running and create the database:
```sql
CREATE DATABASE social_media_db;
```

### 5. Run database migrations
```bash
cd backend
alembic upgrade head
```

### 6. Start the backend
```bash
cd backend
fastapi dev app/main.py
```
Access the API at `http://localhost:8000` and interactive docs at `http://localhost:8000/docs`

### Frontend Setup

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Configure environment variables
Create a `.env.local` file in the `frontend/` directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. Start the frontend
```bash
npm run dev
```
Access the app at `http://localhost:3000`

## Production Deployment

**Backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

## API Endpoints

### Authentication
- `POST /users` - Create new user account
- `POST /login` - Login and receive JWT token

### Posts
- `GET /posts` - List all posts (with vote counts, search, pagination)
- `GET /posts/{id}` - Get specific post with vote count
- `POST /posts` - Create new post (requires auth)
- `PUT /posts/{id}` - Update post (owner only)
- `DELETE /posts/{id}` - Delete post (owner only)

### Voting
- `POST /vote` - Vote on a post
  - `{"post_id": 1, "dir": 1}` - Add vote
  - `{"post_id": 1, "dir": 0}` - Remove vote

### Users
- `GET /users` - List all users (requires auth)
- `GET /users/{id}` - Get user by ID (requires auth)
- `PUT /users/{id}` - Update user (owner only)
- `DELETE /users/{id}` - Delete user (owner only)

## Key Concepts

### Authorization
All protected endpoints require a valid JWT token in the `Authorization` header:
```
Authorization: Bearer <your_jwt_token>
```

### Voting System
- Use `dir: 1` to upvote a post
- Use `dir: 0` to remove your existing vote
- Each user can vote once per post (enforced by composite primary key)
- Returns 409 Conflict if attempting to vote twice or remove non-existent vote

### Post Visibility
- **Published posts** (`published: true`) - Visible to all authenticated users
- **Unpublished posts** (`published: false`) - Visible only to the post owner

### Ownership Rules
- Users can only update/delete their own posts
- Update/delete attempts on others' posts return 403 Forbidden

## Database Schema

```
users: id (PK), email, password, created_at
posts: id (PK), title, content, category, published, created_at, user_id (FK)
votes: user_id (FK, PK), post_id (FK, PK)
```

## Development

### Database Migrations

Make changes in `backend/app/models.py` then:
```bash
cd backend
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Rolling Back Migrations
```bash
cd backend
alembic downgrade -1  # Rollback one version
```

### Running Tests
```bash
cd backend
pytest
```

## Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   │   ├── routers/     # API routes (auth, posts, users, votes)
│   │   ├── config.py    # Settings management
│   │   ├── database.py  # SQLAlchemy setup
│   │   ├── deps.py      # Dependency injection
│   │   ├── models.py    # ORM models
│   │   ├── oauth2.py    # JWT handling
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── utils.py     # Password hashing
│   ├── alembic/         # Database migrations
│   ├── tests/           # Backend tests
│   └── .env             # Backend config
│
├── frontend/            # Next.js frontend
│   ├── src/
│   │   └── app/         # App Router pages & components
│   └── .env.local       # Frontend config
│
└── docs/                # Documentation
```

## Working with AI Agents

This documentation was `enhanced` via GitHub Copilot (in VSCode), and so the project includes [.github/copilot-instructions.md](.github/copilot-instructions.md) - a comprehensive context file that helps GitHub Copilot and other AI coding agents understand the project's architecture, patterns, and conventions. This enables more accurate code suggestions and faster onboarding (and would save the pain of making an agent understand the context).

## Notes

The `docs/` and `tests/` directories contain personal notes and experiments from the learning process - feel free to explore them for additional insights.