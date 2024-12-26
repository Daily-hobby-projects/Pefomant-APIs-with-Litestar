from litestar import Controller
from datetime import datetime
import dataclasses as dc
import uuid
from litestar import get, post, put, delete
from src.posts.crud import find_post_or_404
from src.data import posts
from src.schemas import PostCreateSchema, PostSchema


class PostController(Controller):
    path = "/posts"

    @get()
    async def get_all_posts(self) -> list[PostSchema]:
        return posts

    @get("/{post_uid:uuid}")
    async def get_post(self, post_uid: uuid.UUID) -> PostSchema:
        post = find_post_or_404(post_uid)
        return post

    @post()
    async def create_post(self, data: PostCreateSchema) -> PostSchema:
        new_post = {
            "uid": uuid.uuid4(),
            "title": data.title,
            "content": data.content,
            "status": data.status,
            "date_created": datetime.now(),
        }

        posts.append(new_post)

        return new_post

    @put("/{post_uid:uuid}")
    async def update_post(
        self, data: PostCreateSchema, post_uid: uuid.UUID
    ) -> PostSchema:
        data_dict = dc.asdict(data)

        post_to_update = find_post_or_404(post_uid)

        for k, v in data_dict.items():
            post_to_update[k] = v

        return post_to_update

    @delete("/{post_uid:uuid}")
    async def delete_post(self, post_uid: uuid.UUID) -> None:
        post_to_delete = find_post_or_404(post_uid)
        posts.remove(post_to_delete)
        return None
