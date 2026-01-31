# AI Agent Instructions - Social Media API

## Project Overview
FastAPI + PostgreSQL social media backend with JWT auth, posts, users, and voting system. Protected endpoints enforce ownership rules for CRUD operations.

## Architecture Patterns

### Dependency Injection (Critical)
All route dependencies use `Annotated` type aliases defined in [app/deps.py](app/deps.py):
- `DBSession` - SQLAlchemy session for database queries
- `CurrentUser` - Authenticated user from JWT token (auto-validates)
- `PasswordRequestForm` - OAuth2 form data for login

Example usage:
```python
def create_post(post: schemas.PostCreate, db: deps.DBSession, current_user: deps.CurrentUser):
    new_post = models.Post(**post.model_dump(), user_id=current_user.id)
```

### Pydantic Schema Split
Schemas follow a strict hierarchy ([app/schemas.py](app/schemas.py)):
- `Base` schemas: shared fields (e.g., `UserBase` with email)
- `Create` schemas: inherit Base + add password/sensitive fields
- `Response` schemas: inherit Base + add DB fields (id, timestamps) + set `from_attributes=True`

### Authorization Pattern
All protected routes check ownership manually - **no middleware/decorators**:
```python
if post.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized...")
```

### Vote System Logic
Votes use composite primary key (user_id, post_id). Direction field:
- `dir: 1` = add vote (raises 409 if already exists)
- `dir: 0` = remove vote (raises 409 if not exists)
See [app/routers/vote.py](app/routers/vote.py#L25-L38) for exact logic.

### Query Pattern with Counts
Posts endpoints join votes and return counts (see [app/routers/post.py](app/routers/post.py#L31-L44)):
```python
db.query(models.Post, func.count(models.Vote.post_id).label("vote_count"))
  .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
  .group_by(models.Post.id)
```
Response schema is `PostWithVotes` containing nested `Post` object.

## Configuration & Environment

### Settings Management
[app/config.py](app/config.py) uses `pydantic-settings` to load from `.env`:
- Database: `db_username`, `db_password`, `db_hostname`, `db_port`, `db_name`
- JWT: `jwt_secret_key`, `jwt_algorithm`, `jwt_expire_time` (minutes)

### Database URL Construction
Connection string built as: `postgresql+psycopg://{user}:{pass}@{host}:{port}/{db}`

## Developer Workflows

### Database Migrations
**Always use Alembic** - never `Base.metadata.create_all()`:
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```
Migration order: posts → users → user_id FK → votes

### Running the Application
**Development:**
```bash
fastapi dev app/main.py
```

**Production:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Authentication Flow
1. POST to `/login` with OAuth2 form (username=email, password)
2. Receive JWT token valid for `jwt_expire_time` minutes
3. Include in requests as `Authorization: Bearer <token>`
4. Token decoded/validated automatically via `oauth2.get_current_user()`

## Critical Conventions

### Password Hashing
Use `pwdlib` (not bcrypt/passlib) - see [app/utils.py](app/utils.py):
```python
from .utils import get_password_hash, verify_password
```

### Router Organization
All routers use prefixes and tags:
```python
router = APIRouter(prefix="/posts", tags=['Posts'])
```

### Error Handling
Pre-defined exceptions in [app/exceptions.py](app/exceptions.py) - use `credentials_exception` for auth failures.

### Post Visibility Logic
Posts are visible if:
- `published=True` OR `user_id == current_user.id`

Implemented as: `or_(models.Post.user_id == current_user.id, models.Post.published == True)`
