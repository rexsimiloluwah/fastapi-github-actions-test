import uvicorn
from database import Base, engine
from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth as auth_router, bucket as bucket_router, user as user_router

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Demo FastAPI and Github actions app",
    version="0.01",
    description="A FastAPI app deployed to Heroku with a Github actions CI/CD pipeline.",
    contact={
        "name": "Similoluwa Okunowo",
        "url": "https://simiokunowo.netlify.app",
        "email": "rexsimiloluwa@gmail.com",
    },
)

BASE_URL = "/api/v1"

app.include_router(auth_router.router, tags=["Auth"], prefix=BASE_URL)
app.include_router(bucket_router.router, tags=["Bucket"], prefix=BASE_URL)
app.include_router(user_router.router, tags=["User"], prefix=BASE_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
