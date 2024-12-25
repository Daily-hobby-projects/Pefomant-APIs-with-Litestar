from litestar import Litestar, get


@get('/')
async def index() -> dict:
    return {
        "message" :"Hello World"
    }


app = Litestar(
    route_handlers=[index]
)