import uuid
import dataclasses
from litestar import Controller, get, post, put, delete, status_codes
from litestar.exceptions import NotFoundException, InternalServerException
from sqlalchemy.ext.asyncio import AsyncSession
from src.comments.crud import (
    create_comment,
    delete_comment_by_uid,
    read_all_post_comments,
    update_comment,
)
from src.models import Comment
from src.schemas import CommentCreateSchema, CommentSchema


def serialize_comment(comment: Comment) -> CommentSchema:
    return CommentSchema(
        id=comment.id,
        username=comment.username,
        content=comment.content,
        status=comment.status,
        date_created=comment.date_created,
        date_updated=comment.date_updated,
        post_id=comment.post_id,
    )


class CommentController(Controller):

    @get("/posts/{post_uid:uuid}/comments")
    async def get_post_comments(
        self, session: AsyncSession, post_uid: uuid.UUID
    ) -> list[CommentSchema]:
        """Get post comments"""
        comments = await read_all_post_comments(session, post_id=post_uid)

        print("comment: {}".format(comments))

        return [serialize_comment(c) for c in comments]

    @post("/posts/{post_uid:uuid}/comments")
    async def create_comment_on_post(
        self, session: AsyncSession, data: CommentCreateSchema, post_uid: uuid.UUID
    ) -> CommentSchema:
        """Create comment on post"""
        data_dict = dataclasses.asdict(data)
        data_dict["status"] = data.status.value
        new_comment = await create_comment(session, post_id=post_uid, data=data_dict)
        return serialize_comment(new_comment)

    @put("/posts/{post_uid:uuid}/comments/{comment_uid:uuid}")
    async def edit_comment(
        self, session: AsyncSession, comment_uid: uuid.UUID, data: CommentCreateSchema
    ) -> CommentSchema:
        """Edit comment"""
        data_dict = dataclasses.asdict(data)
        data_dict["status"] = data.status.value
        updated_comment = await update_comment(
            session=session, comment_id=comment_uid, data=data_dict
        )

        if not updated_comment:
            raise NotFoundException(
                detail="Comment not found", status_code=status_codes.HTTP_404_NOT_FOUND
            )

        return serialize_comment(updated_comment)

    @delete("/posts/{post_uid:uuid}/comments/{comment_uid:uuid}")
    async def delete_comment(
        self, session: AsyncSession, comment_uid: uuid.UUID
    ) -> None:
        """Delete comment"""
        comment_deleted = await delete_comment_by_uid(session, comment_id=comment_uid)
        if not comment_deleted:
            raise NotFoundException(
                detail="Comment not found", status_code=status_codes.HTTP_404_NOT_FOUND
            )
        return None
