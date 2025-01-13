from litestar import Litestar, get
from src.posts.routes import PostController
from src.db import create_session, init_db

@get("/")
async def index() -> dict:
    return {"message": "Hello World"}

app = Litestar(
    route_handlers=[index, PostController],
    lifespan=[init_db],
    dependencies={
        "session": create_session
    }
)
