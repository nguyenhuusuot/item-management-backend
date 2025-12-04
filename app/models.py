from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class UserDB(Base):
    __tablename__ = "users"
    # khóa chính, tự tăng
    id = Column(Integer,primary_key=True, index=True)
    # Không được trùng tên
    username = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)
    phone_number = Column(String, default="Chua co so")
    # Mối quan hệ tới bảng ItemDB, owner 
    # cascade="all, delete-orphan" là nếu xóa user thì hãy xóa luôn items thuộc về user đó
    items = relationship("ItemDB", back_populates="owner", cascade="all, delete-orphan")

class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    des = Column(String)
    # Liên kết tới bảng users , khóa ngoại users.id
    owner_id = Column(Integer, ForeignKey("users.id"))
    # Mối quan hệ tới bảng UserDB, items
    owner = relationship("UserDB", back_populates="items")
 

