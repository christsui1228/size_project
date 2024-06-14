from fastapi import FastAPI,Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.routers import file

app=FastAPI()

#define origins

origins = [
    "http://localhost:5173",  # 替换为你的前端地址
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return{"message":"Welcome to the FastAPI application!"}

@app.get("/favicon.ico",include_in_schema=False)
async def favicon():
    # 提供一个默认的 favicon 响应
    return FileResponse("favicon.ico")

app.include_router(file.router)