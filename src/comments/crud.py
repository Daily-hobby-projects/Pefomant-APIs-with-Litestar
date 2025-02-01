from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

from src.models import Comment, Post
from src.posts.crud import get_single_post


async def create_comment(session: AsyncSession, post_id: uuid.SafeUUID, data: dict):
    post = await get_single_post(session=session, post_uid=post_id)
    new_comment = Comment(
        username=data["username"],
        content=data["content"],
        status=data["status"],
    )
    post.comments.append(new_comment)
    await session.commit()
    session.refresh(new_comment)
    return new_comment


async def read_all_post_comments(session: AsyncSession, post_id: uuid.UUID):
    post = await get_single_post(session=session, post_uid=post_id)
    return post.comments


async def get_single_comment(session: AsyncSession, comment_id: uuid.UUID):
    query = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_comment(session: AsyncSession, comment_id: uuid.UUID, data: dict):
    comment = await get_single_comment(session=session, comment_id=comment_id)
    if comment is None:
        return None
    for k, v in data.items():
        if hasattr(comment, k):
            setattr(comment, k, v)
    await session.commit()

    await session.refresh(comment)
    return comment


async def delete_comment_by_uid(session: AsyncSession, comment_id: uuid.UUID):
    comment = await get_single_comment(session=session, comment_id=comment_id)

    if comment is None:
        return False

    await session.delete(comment)

    await session.commit()
    return True
