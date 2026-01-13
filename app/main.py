from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from random import randrange
from .database import engine,  get_db
from sqlalchemy.orm import Session
from . import models
import psycopg2
from psycopg2.extras import RealDictCursor
import time
 

models.Base.metadata.create_all(bind=engine) 
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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}
   

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI!"}

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"posts": posts}

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create_post(post: Post , db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",(new_post.title, new_post.content, new_post.published))
    #created_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created successfully", "post": new_post}

@app.get("/posts/latest")    
def get_latest_post(): 
    cursor.execute(""" SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    post = cursor.fetchone()
    return {"post": post}
  
@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
   # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
   # post = cursor.fetchone()
   post = db.query(models.Post).filter(models.Post.id == id).first()
   if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
   return {"post": post}

@app.delete("/posts/{id}")
def delete_post(id: int , db: Session = Depends(get_db)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(id: int , updated_post: Post , db: Session = Depends(get_db)):
   # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,
   #                (updated_post.title, updated_post.content, updated_post.published, str(id)) )
   # result = cursor.fetchone()
   post_query = db.query(models.Post).filter(models.Post.id == id)
   post = post_query.first()
   if post is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
   post_query.update(updated_post.dict(), synchronize_session=False)
   db.commit()
   return {"message": "Post updated successfully"} 
    