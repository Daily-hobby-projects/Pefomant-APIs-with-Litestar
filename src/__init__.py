from litestar import Litestar, get
from src.posts.routes import PostController

@get("/")
async def index() -> dict:
    return {"message": "Hello World"}

app = Litestar(route_handlers=[index, PostController])
