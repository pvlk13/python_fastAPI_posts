from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine,  get_db
from sqlalchemy.orm import Session
from . import models
from .routers import posts, users , auth
import psycopg2
from psycopg2.extras import RealDictCursor
import time
 
from .password import ph
models.Base.metadata.create_all(bind=engine) 
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
  
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
   

