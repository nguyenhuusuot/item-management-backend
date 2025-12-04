from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from app.core.config import settings
import redis

# đường dẫn database
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# tạo cổng kết nối
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# tạo sesionlocal
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

# mọi model bảng đều kế thừa từ class này
Base = declarative_base()
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

# Lấy DB session an toàn
def get_db():
    db = SessionLocal()
    try:
        yield db # trả về phiên làm việc cho request
    finally:
        db.close() # luôn đóng kết nối khi request chạy xong
