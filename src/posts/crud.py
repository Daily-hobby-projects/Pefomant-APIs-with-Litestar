import uuid
from litestar import status_codes
from litestar.exceptions import HTTPException
from src.data import posts

def find_post_or_404(uuid: uuid.UUID):
    for post in posts:
        if post["uid"] == uuid:
            return post
    raise HTTPException(
        detail="Post not found", status_code=status_codes.HTTP_404_NOT_FOUND
    )
