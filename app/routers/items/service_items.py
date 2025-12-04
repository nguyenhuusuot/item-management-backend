from sqlalchemy import desc
from sqlalchemy.orm import Session
from app import schemas, models
from app.models import UserDB


def create_item_by_id_user_service(db : Session, user_id : int, item : schemas.Item):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        return None
    # tạo item mới, gắn owner_id = user_id
    db_item = models.ItemDB(**item.model_dump(), owner_id = user_id)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items_by_user(db : Session, user_id : int, skip : int = 0, limit : int = 100):
    return db.query(models.ItemDB).filter(models.ItemDB.owner_id == user_id).offset(skip).limit(limit).all()

def get_item_service(db : Session, search : str | None = None ,skip: int = 0 , limit: int = 100):
    query = db.query(models.ItemDB)

    if search:
        #                    where title like search
        query = query.filter(models.ItemDB.title.contains(search))

    # Sắp xếp : id item mới nhất lên đầu ( giảm dần )
    query = query.order_by(desc(models.ItemDB.id))
    # Phân trang : bỏ qua 'skip' dòng , lấy 'limit' dòng
    items = query.offset(skip).limit(limit).all() 
    return items

def update_user_item(db : Session, user_id : int, item_id : int, item_update : schemas.Item):
    db_item = db.query(models.ItemDB).filter(
        models.ItemDB.id == item_id,
        models.ItemDB.owner_id == user_id
    ).first()

    if db_item :
        db_item.title = item_update.title
        if item_update.des is not None:
            db_item.des = item_update.des
    
        db.commit()
        db.refresh(db_item)
    
    return db_item

def delete_item_user(db : Session, user_id: int, item_id: int):
    db_item = db.query(models.ItemDB).filter(
        models.ItemDB.id == item_id,
        models.ItemDB.owner_id == user_id
    ).first()

    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    
    return False


