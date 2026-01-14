
from ..database import engine,  get_db 
from sqlalchemy.orm import Session
from .. import models, schemas

from fastapi import FastAPI, Body, Response, status, HTTPException, Depends , APIRouter
from typing import List
from .. import oauth

router = APIRouter(
    prefix="/posts",
    
)

@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate , db: Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user) ):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",(new_post.title, new_post.content, new_post.published))
    #created_post = cursor.fetchone()
    #conn.commit()
    print(get_current_user)
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/latest" , response_model=schemas.PostResponse)    
def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post
    
  
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
   # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
   # post = cursor.fetchone()
   post = db.query(models.Post).filter(models.Post.id == id).first()
   if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
   return post

@router.delete("/{id}")
def delete_post(id: int , db: Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int , updated_post: schemas.PostCreate , db: Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user)):
   # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,
   #                (updated_post.title, updated_post.content, updated_post.published, str(id)) )
   # result = cursor.fetchone()
   post_query = db.query(models.Post).filter(models.Post.id == id)
   post = post_query.first()
   if post is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
   post_query.update(updated_post.dict(), synchronize_session=False)
   db.commit()
   return post_query.first()