from fastapi import FastAPI, Request
from app import models
from app.database import engine
from app.routers.items import controller_items
from app.routers.users import controller_users
from app.routers.auth import controller_auth
from fastapi.middleware.cors import CORSMiddleware
import time
# Tạo bảng trong DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request : Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(process_time)
    print(f"{request.url.path} took {process_time:.6f}s")
    return response

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    # domain thật
    "https://mydomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ["*"], #Cho phép các methods : GET, PUT, POST
    allow_headers =["*"], # cho phép các header : Auth, content
    expose_headers=["X-Process-Time"]
)

# Gắn các router vào ứng dụng chính
app.include_router(controller_items.router)
app.include_router(controller_users.router)
app.include_router(controller_auth.router)

@app.get("/")
def root():
    return {"message": "Hello World! Cấu trúc dự án mới xịn xò."}