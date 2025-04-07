from fastapi import FastAPI
import uvicorn
from core.config import settings
from core.database import init_db
from routers.post import router as post_router
from routers.user import router as user_router


app = FastAPI(title=settings.app_name)

@app.get("/")
def main():
    return ("Hello")

app.include_router(user_router)
app.include_router(post_router)
init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)