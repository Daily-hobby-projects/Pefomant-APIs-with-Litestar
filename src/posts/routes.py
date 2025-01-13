from litestar import Controller
from datetime import datetime
import dataclasses as dc
import uuid
from litestar import get, post, put, delete, status_codes
from litestar.exceptions import NotFoundException, InternalServerException
from src.models import Post
from src.posts.crud import delete_post_by_uid, find_post_or_404, list_posts, get_single_post, create_new_post, update_post_by_uid
from src.data import posts
from src.schemas import PostCreateSchema, PostSchema, PostStatusEnum
from sqlalchemy.ext.asyncio import AsyncSession


def serialize_post(post: Post) -> PostSchema:
    """serialize post db object to post schema object"""
    return PostSchema(
        id=post.id,
        title=post.title,
        content=post.content,
        status=post.status,
        date_created=post.date_created,
        date_updated=post.date_updated,
    )


class PostController(Controller):
    path = "/posts"

    @get()
    async def get_all_posts(
        self, session: AsyncSession, status: PostStatusEnum = PostStatusEnum.PUBLISHED
    ) -> list[PostSchema]:
        posts = await list_posts(session=session, status=status.value)
        return [serialize_post(post) for post in posts]

    @get("/{post_uid:uuid}")
    async def get_post(self, session: AsyncSession, post_uid: uuid.UUID) -> PostSchema:
        try:
            post = await get_single_post(session,post_uid)
            return serialize_post(post)
        except Exception as e:
            print(e)
            raise NotFoundException(
                detail="Post Not Found",
                status_code= status_codes.HTTP_404_NOT_FOUND
            )

    @post()
    async def create_post(
        self, session: AsyncSession, data: PostCreateSchema
    ) -> PostSchema:
        try:
            data_dict = dc.asdict(data)
            data_dict['status'] = data.status.value

            new_post = await create_new_post(session, data_dict)

            return serialize_post(new_post)
        except Exception as e:
            print(e)
            raise InternalServerException(
                detail="Something went wrong",
                status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @put("/{post_uid:uuid}")
    async def update_post(
        self, session: AsyncSession, data: PostCreateSchema, post_uid: uuid.UUID
    ) -> PostSchema:
        data_dict = dc.asdict(data)
        data_dict['status'] = data.status.value
        post_to_update = await update_post_by_uid(session,post_uid,data_dict)

        return serialize_post(post_to_update)

    @delete("/{post_uid:uuid}")
    async def delete_post(self, session: AsyncSession, post_uid: uuid.UUID) -> None:
        await delete_post_by_uid(session,post_uid)
        return None
