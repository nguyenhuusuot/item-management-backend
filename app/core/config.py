from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #Khai báo các biến cần lấy tên cần trùng với file .env
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256" # Có thể đặt giá trị mặc định
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    # Cấu hình tim file .env
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()