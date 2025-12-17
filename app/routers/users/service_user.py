from sqlalchemy.orm import Session
from ... import schemas, models
from app.core.security import hash_password

def create_user_sevice(db : Session, user : schemas.User):
    
    db_user = user.model_dump()
    db_user["password"] = hash_password(db_user["password"])
    # Tạo object model từ dữ liệu
    # user.model_dump() sẽ trả về dict dữ liệu của user
    # **dict sẽ giải nén dict thành các tham số để truyền vào constructor của SQLAlchemy model.
    db_user = models.UserDB(**db_user)
    db.add(db_user) 

    # Lưu vào db
    db.commit()
    # Lấy lại dữ liệu từ DB để có ID vừa sinh ra
    db.refresh(db_user)
    return db_user

def get_user_by_id_service(db : Session, user_id : int):
    return db.query(models.UserDB).filter(models.UserDB.id == user_id).first()

def get_user_by_email_sevice(db : Session, email : str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def get_all_user_sevice(db : Session , skip : int = 0, limit : int= 100):
    return db.query(models.UserDB).offset(skip).limit(limit).all()

def get_user_by_username_service(db : Session, username : str):
    return db.query(models.UserDB).filter(models.UserDB.username == username).first()

def delete_user_by_id(db : Session, user_id : int):
    db_user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user) # đánh dấu xóa
    db.commit()     # xóa thật
    return True

def update_user_by_id(db: Session, user_id : int, update_data : schemas.Update_User_Schema):
    db_user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    
    # lấy dic các trường mà người dùng gửi lên 
    update_dic = update_data.model_dump(exclude_unset=True)
    
    # Tự động lưu các trường có trong update_data tức là các trường mà người dùng nhập vào
    for key, value in update_dic.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user
