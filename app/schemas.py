from pydantic import BaseModel, ConfigDict,EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class User_Schema(BaseModel):
    id: int 
    username: str
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

class Update_User_Schema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    model_config = ConfigDict(from_attributes=True)


class Item(BaseModel):
    title: str
    des: str 

class Item_Schema(Item):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


class UserWithItems(BaseModel):
    id: int
    username: str
    email: str
    items: list[Item_Schema] = []
    model_config = ConfigDict(from_attributes=True)