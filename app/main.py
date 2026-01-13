from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from random import randrange
from .database import engine,  get_db
from sqlalchemy.orm import Session
from . import models, schemas
from .routers import posts, users
import psycopg2
from psycopg2.extras import RealDictCursor
import time
 
from .password import ph
models.Base.metadata.create_all(bind=engine) 
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
  
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
   

# @app.get("/")
# async def root():
#     return {"message": "Hello World from FastAPI!"}

# @app.get("/posts", response_model=List[schemas.PostResponse])
# async def get_posts(db: Session = Depends(get_db)):
#     #cursor.execute("""SELECT * FROM posts""")
#     #posts = cursor.fetchall()
#     posts = db.query(models.Post).all()
#     return  posts

# @app.post("/posts" , status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
# def create_post(post: schemas.PostCreate , db: Session = Depends(get_db)):
#     #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",(new_post.title, new_post.content, new_post.published))
#     #created_post = cursor.fetchone()
#     #conn.commit()
#     new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return  new_post

# @app.get("/posts/latest" , response_model=schemas.PostResponse)    
# def get_latest_post(db: Session = Depends(get_db)):
#     latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
#     return latest_post
    
  
# @app.get("/posts/{id}", response_model=schemas.PostResponse)
# def get_post(id: int, response: Response, db: Session = Depends(get_db)):
#    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
#    # post = cursor.fetchone()
#    post = db.query(models.Post).filter(models.Post.id == id).first()
#    if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
#    return post

# @app.delete("/posts/{id}")
# def delete_post(id: int , db: Session = Depends(get_db)):
#     #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     #deleted_post = cursor.fetchone()
#     deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
#     db.delete(deleted_post)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# @app.put("/posts/{id}", response_model=schemas.PostResponse)
# def update_post(id: int , updated_post: schemas.PostCreate , db: Session = Depends(get_db)):
   # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,
   #                (updated_post.title, updated_post.content, updated_post.published, str(id)) )
   # result = cursor.fetchone()
#    post_query = db.query(models.Post).filter(models.Post.id == id)
#    post = post_query.first()
#    if post is None:
#          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
#    post_query.update(updated_post.dict(), synchronize_session=False)
#    db.commit()
#    return post_query.first()

# @app.post("/users" , status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
# def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):
#     #hash the password - user.password
#     hashed_password = ph.hash(user.password)
#     new_user = models.User(email=user.email, password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return  new_user

# @app.get("/users/{id}", response_model=schemas.UserResponse)
# def get_user(id: int, db: Session = Depends(get_db)):
#    user = db.query(models.User).filter(models.User.id == id).first()
#    if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
#    return user

# @app.get("/users", response_model=List[schemas.UserResponse])
# def get_all_users(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users


# @app.put("/users/{id}", response_model=schemas.UserResponse)
# def update_users(id: int ,user: schemas.UserCreate, db: Session = Depends(get_db)):
#     user_query = db.query(models.User).filter(models.User.id == id)
#     updated_user = user_query.first()
#     if updated_user is None:
#          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    
#     # 3. CONVERT the Pydantic model to a dictionary
#     update_data = user.model_dump() # use .dict() if on older Pydantic
    
#     # 4. HASH the new password before updating the DB
#     update_data["password"] = ph.hash(update_data["password"])
#     user_query.update(update_data, synchronize_session=False)
#     db.commit()
#     return user_query.first()
    #