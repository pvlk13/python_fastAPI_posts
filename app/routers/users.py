
from ..database import engine,  get_db 
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends , APIRouter
from typing import List
from .. password import ph


router = APIRouter(
    prefix="/users",
)

@router.post("/" , status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_password = ph.hash(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.id == id).first()
   if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
   return user

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.put("/{id}", response_model=schemas.UserResponse)
def update_users(id: int ,user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    updated_user = user_query.first()
    if updated_user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    
    # 3. CONVERT the Pydantic model to a dictionary
    update_data = user.model_dump() # use .dict() if on older Pydantic
    
    # 4. HASH the new password before updating the DB
    update_data["password"] = ph.hash(update_data["password"])
    user_query.update(update_data, synchronize_session=False)
    db.commit()
    return user_query.first()