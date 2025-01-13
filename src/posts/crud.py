import uuid
from litestar import status_codes
from litestar.exceptions import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.data import posts
from src.models import Post


def find_post_or_404(uuid: uuid.UUID):
    for post in posts:
        if post["uid"] == uuid:
            return post
    raise HTTPException(
        detail="Post not found", status_code=status_codes.HTTP_404_NOT_FOUND
    )


async def list_posts(session: AsyncSession, status: str = None) -> list[Post]:
    """get all posts"""
    query = select(Post).order_by(desc(Post.date_created))

    if status:
        query = query.filter_by(status=status)

    result = await session.execute(query)

    return result.scalars().all()


async def get_single_post(session: AsyncSession, post_uid: uuid.UUID) -> Post:
    """get single post"""
    query = select(Post).where(Post.id == post_uid)
    result = await session.execute(query)
    return result.scalars().one()


async def create_new_post(session: AsyncSession, data: dict) -> Post:
    """create post"""
    new_post = Post(**data)

    session.add(new_post)

    await session.commit()

    return new_post


async def update_post_by_uid(session: AsyncSession, post_uid: uuid.UUID, data: str) -> Post:
    post_to_update = await get_single_post(session, post_uid)

    for k, v in data.items():
        if hasattr(post_to_update, k):
            setattr(post_to_update, k, v)

    await session.commit()

    return post_to_update

async def delete_post_by_uid(session: AsyncSession, post_uid: uuid.UUID) -> Post:
    post_to_delete = await get_single_post(session, post_uid)

    await session.delete(post_to_delete)

    await session.commit()

    return None