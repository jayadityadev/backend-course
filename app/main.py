from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = FastAPI()

class Post(BaseModel):
    id : int | None = None
    title: str
    content: str
    category: str = "Generic"
    published: bool = True

try:
    conn = psycopg.connect(
        dbname=getenv('DB_NAME'), user=getenv('DB_USER'), password=getenv('DB_PASS'), row_factory=dict_row
    )
    table_name = "posts"
    print("DB connected!")
except psycopg.OperationalError as err:
    print(f"DB Error: {err}")
except psycopg.ProgrammingError as err:
    print(f"DB Error: {err}")

@app.get("/")
def read_root():
    return {"working": True}

# CRUD - C
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    with conn.cursor() as cur:
        cur.execute(
            f"""INSERT INTO {table_name} (title, content, category, published) 
            VALUES (%s, %s, %s, %s) RETURNING *""",
            (post.title, post.content, post.category, post.published)
        )
        new_post = cur.fetchone()
        if new_post is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create post"
            )
        conn.commit()
        return {"detail": "Post created successfully!", "data": new_post}

# CRUD - R
@app.get("/posts")
def get_posts():
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT * FROM {table_name} ORDER BY created_at DESC"""
        )
        return cur.fetchall()

# CRUD - R
@app.get("/posts/{id}") # path parameter
def get_post(id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT * FROM {table_name} WHERE id = %s""",
            (id,)
        )
        row = cur.fetchone()
        if row is None:
            raise HTTPException(
                status_code=404,
                detail=f"Post with id {id} not found!"
            )
        return row

# CRUD - U
@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
    with conn.cursor() as cur:
        cur.execute(
            f"""UPDATE {table_name}
            SET title=%s, content=%s, category=%s, published=%s WHERE id=%s RETURNING *""",
            (post.title, post.content, post.category, post.published, id)
        )
        updated_post = cur.fetchone()
        if updated_post is None:
            raise HTTPException(
                status_code=404,
                detail=f"Post with id {id} not found!"
            )
        conn.commit()
        return

# CRUD - D
@app.delete("/posts/{id}")
def delete_posts(id: int):
    with conn.cursor() as cur:
        cur.execute(
            f"""DELETE FROM {table_name} WHERE id=%s RETURNING *""",
            (id,)
        )
        deleted_post = cur.fetchone()
        if deleted_post is None:
            raise HTTPException(
                status_code=404,
                detail=f"Post with id {id} not found!"
            )
        conn.commit()
        return {"detail": "Post deleted successfully!", "data": deleted_post}
