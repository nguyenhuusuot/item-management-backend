from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database, schemas
from app.routers.users import service_user
from app.core import security


def login_for_accsess_token_service(
    from_data : OAuth2PasswordRequestForm = Depends(),
    db : Session = Depends(database.get_db)
):
    # Tìm user trong DB
    user = service_user.get_user_by_username_service(db=db,username=from_data.username)

    if not user or not security.verify_password(from_data.password, user.password):
        return None
    
    access_token = security.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}