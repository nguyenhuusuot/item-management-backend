from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database, schemas
from app.routers.users import service_user
from app.core import security
from app.routers.auth import service_auth

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/token")
async def login_ccsess_token(
    from_data : OAuth2PasswordRequestForm = Depends(),
    db : Session = Depends(database.get_db)
):
    # Tìm user trong DB
    token = service_auth.login_for_accsess_token_service(from_data=from_data, db = db)
    
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    return token