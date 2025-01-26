from datetime import datetime
import uuid
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.schemas import CommentStatusEnum, PostStatusEnum


class Base(DeclarativeBase): ...

class Post(Base):
    __tablename__ = "blog_posts"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, unique=True, default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        nullable=False, default=PostStatusEnum.DRAFT.value
    )
    date_created: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    date_updated: Mapped[datetime] = mapped_column(nullable=True)
    comments: Mapped[list["Comment"]] = relationship(back_populates="post",lazy="selectin")
    def __repr__(self):
        return f"<Post created at {self.date_created}>"


class Comment(Base):
    __tablename__ = "blog_comments"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, unique=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        nullable=False, default=CommentStatusEnum.PUBLIC.value
    )
    date_created: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    date_updated: Mapped[datetime] = mapped_column(nullable=True)
    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("blog_posts.id"), nullable=False
    )
    post: Mapped[Post] = relationship(back_populates="comments")


    def __repr__(self):
        return f"<Comment {self.id}>"