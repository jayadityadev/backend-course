# Social Media API

A production-ready FastAPI backend application for a social media platform with user authentication, post management, and voting functionality.

## Features

- **User Authentication** - JWT-based authentication with secure password hashing (pwdlib)
- **Post Management** - Full CRUD operations with ownership-based authorization
- **Voting System** - Upvote/downvote functionality with vote count aggregation
- **Post Visibility** - Published posts visible to all, unpublished posts visible to owners only
- **Search & Pagination** - Query posts by title with limit/offset pagination
- **Database Migrations** - Alembic-managed schema versioning

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens (PyJWT) + OAuth2
- **Password Hashing**: pwdlib (Argon2)
- **Migrations**: Alembic
- **Validation**: Pydantic v2

## Quick Start

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

pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root:

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
alembic upgrade head
```

### 6. Start the application

**Development:**
```bash
fastapi dev app/main.py
```
Access the API at `http://localhost:8000` and interactive docs at `http://localhost:8000/docs`

**Production:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
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

### Creating New Migrations
Make the required changes in `app/models.py` and let alembic handle the database.
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Rolling Back Migrations
```bash
alembic downgrade -1  # Rollback one version
```

## Project Structure

```
app/
├── routers/          # API route handlers
│   ├── auth.py       # Login endpoint
│   ├── post.py       # Post CRUD operations
│   ├── user.py       # User management
│   └── vote.py       # Voting system
├── config.py         # Settings management (pydantic-settings)
├── database.py       # SQLAlchemy setup
├── deps.py           # Dependency injection type aliases
├── exceptions.py     # Reusable exception definitions
├── models.py         # SQLAlchemy ORM models
├── oauth2.py         # JWT token creation/validation
├── schemas.py        # Pydantic request/response models
└── utils.py          # Password hashing utilities
```

## Working with AI Agents

This documentation was `enhanced` via GitHub Copilot (in VSCode), and so the project includes [.github/copilot-instructions.md](.github/copilot-instructions.md) - a comprehensive context file that helps GitHub Copilot and other AI coding agents understand the project's architecture, patterns, and conventions. This enables more accurate code suggestions and faster onboarding (and would save the pain of making an agent understand the context).

## Notes

The `docs/` and `tests/` directories contain personal notes and experiments from the learning process - feel free to explore them for additional insights.