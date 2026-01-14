
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from .. import models
from .. import oauth

router = APIRouter(tags=["Authentication"])


from ..password import verify_password


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

	is_password_valid = verify_password(user_credentials.password, user.password)
	if not is_password_valid:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
	
	access_token = oauth.create_access_token(data={"user_id": user.id})
	return {"access_token": access_token, "token_type": "bearer"}