from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import UserDB
from app.schemas import Update_User_Schema,User_Schema,User
from app.database import get_db
from app import models,schemas,database
from app.routers.users import service_user


router = APIRouter(
    prefix="/users",  #API bắt đầu url bằng users
    tags=["users"]      #gom nhóm trên docs
)

@router.post("/", response_model=schemas.User_Schema)
async def create_user(user : schemas.User, db : Session = Depends(database.get_db)):
    db_user = service_user.get_user_by_email_sevice(db = db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400 , detail="Email already registered")

    return service_user.create_user_sevice(db=db, user=user)



@router.get("/", response_model=list[schemas.User_Schema])
async def get_all_user(skip : int = 0, limit : int = 100 ,db: Session = Depends(database.get_db)):
    db_users = service_user.get_all_user_sevice(db = db, skip=skip, limit=limit)
    if db_users is None:
        raise HTTPException(status_code=404,detail="Users not found")

    return service_user.get_all_user_sevice(db = db,skip= skip, limit=limit)    

# tìm id và trả về nếu không có thì trả về 404
@router.get("/{user_id}", response_model=schemas.User_Schema)
async def get_user_by_id(user_id: int, db : Session = Depends(database.get_db)):
    # .filter(UserDB.id == user_id): Lọc theo điều kiện
    # .filter(UserDB.id == user_id): Lọc theo điều kiện
    db_user = service_user.get_user_by_id_service(db = db,user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return service_user.get_user_by_id_service(db = db,user_id=user_id)

# Xóa user bằng id
@router.delete("/{user_id}")
async def delete_user_by_id(user_id : int, db : Session = Depends(database.get_db)):
    db_user = service_user.delete_user_by_id(db = db, user_id= user_id)

    if db_user is False:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message":"Deleted item succeccfully"}


@router.patch("/{user_id}")
async def update_user(user_id : int,update_data: schemas.Update_User_Schema = Body(...), db : Session = Depends(database.get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code= 404, detail="User not found")
    
    db_user = service_user.update_user_by_id(db = db, user_id = user_id,update_data= update_data)

    return {"message":"Updated user successfully "}
