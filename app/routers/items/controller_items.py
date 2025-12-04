from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.models import UserDB, ItemDB
from app import models,schemas,database
from app.schemas import Item_Schema, UserWithItems
from app.routers.items import service_items
from app.routers.users import service_user
from app import dependencies
from app import utils
import json
from fastapi.encoders import jsonable_encoder
from app.database import redis_client




router = APIRouter(
    prefix="/items",  #API bắt đầu url bằng items
    tags=["items"]      #gom nhóm trên docs
)

@router.post("/", response_model=schemas.Item_Schema)
async def create_item(
    *,
    item : schemas.Item,
    current_user : models.UserDB = Depends(dependencies.get_current_user), 
    db : Session = Depends(database.get_db),
    background_tasks : BackgroundTasks,
):
    new_item = service_items.create_item_by_id_user_service(db=db, user_id=current_user.id,item=item)

    background_tasks.add_task(
    utils.fake_send_email,
    current_user.email,
    f"Created item successfully : {item.title}"
)
    return new_item

@router.get("/users_with_items/", response_model=list[schemas.Item_Schema])
async def users_with_items(*,current_user : models.UserDB = Depends(dependencies.get_current_user),skip: int = 0, limit :int =100,db : Session = Depends(database.get_db)):
    return service_items.get_items_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/",response_model=list[schemas.Item_Schema])
async def view_item(skip : int = 0, limit : int = 100, search : str | None = Query(None, title="Search by title"), db: Session = Depends(database.get_db)):
    cache_key = f"items_{skip}_{limit}_{search}"

    cached_data = redis_client.get(cache_key)

    if cached_data:
        return json.loads(cached_data)
    
    items = service_items.get_item_service(db= db, search=search,skip= skip, limit= limit)
    data_to_save = json.dumps(jsonable_encoder(items))

    redis_client.set(cache_key,data_to_save,ex=60)
    return items

@router.put("/}", response_model=schemas.Item_Schema)
async def update_item_by_user(*,item_id : int, current : models.UserDB = Depends(dependencies.get_current_user), item_update : schemas.Item , db : Session = Depends(database.get_db)):
    return service_items.update_user_item(db = db, user_id= current.id, item_id= item_id, item_update= item_update)

@router.delete("/")
async def delete_item_by_user(item_id : int,current_user: models.UserDB = Depends(dependencies.get_current_user), db : Session = Depends(database.get_db)):
    succsess = service_items.delete_item_user(db= db, user_id= current_user.id, item_id= item_id)

    if succsess is False:
        raise HTTPException(status_code=404, detail="Item not found or you are not the owner")
    return {"message":"Deleted item succeccfully"}