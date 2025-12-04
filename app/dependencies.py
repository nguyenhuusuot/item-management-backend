from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app import database, models, schemas
from app.routers.users import service_user
from app.core.config import settings

# cấu hình nơi lấy token tokenURL phải trùng với api login
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
        token: str = Depends(oauth2_schema),
        db : Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        
        payload = jwt.decode(token = token, key=settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        
        username : str = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = service_user.get_user_by_username_service(db=db, username= username)
    if user is None:
        raise credentials_exception

    return user
