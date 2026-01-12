from fastapi import FastAPI, Body, Response, status , HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
class Post(BaseModel):
    
    title: str
    content: str
    published: bool = True
    
while True:    

  try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='vijaya', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
    break
  except Exception as error:
    print("Connecting to database failed")
    print("Error:", error)
    time.sleep(2)    




my_posts = [
    {"title": "First Post", "content": "This is my first post", "id": 1},
    {"title": "Second Post", "content": "This is my second post", "id": 2}]

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI!"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",
                   (new_post.title, new_post.content, new_post.published) )
    created_post = cursor.fetchone()
    conn.commit()
    return {"message": "Post created successfully", "post": created_post}

@app.get("/posts/latest")    
def get_latest_post(): 
    cursor.execute(""" SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    post = cursor.fetchone()
    return {"post": post}
  
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return {"post": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(id: int , updated_post: Post):
    cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,
                   (updated_post.title, updated_post.content, updated_post.published, str(id)) )
    update_post = cursor.fetchone()
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    conn.commit()
    return {"message": "Post updated successfully", "post": update_post}
   