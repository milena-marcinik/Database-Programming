from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///:memory:")
Base = declarative_base()

# association table
post_keywords = Table(
    "post_keywords",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("keyword_id", ForeignKey("keywords.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    posts = relationship(
        "Post", back_populates="author", cascade="all, delete, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete, delete-orphan"
    )
    reactions = relationship(
        "Reaction", back_populates="user", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, second_name={self.last_name})"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    headline = Column(String(255))
    body = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship(User, back_populates="posts")
    keywords = relationship(
        "Keyword",
        secondary=post_keywords,
        back_populates="posts",
    )
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete, delete-orphan"
    )
    reactions = relationship(
        "Reaction", back_populates="post", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"Post(id={self.id}, author={self.author})"


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    keyword = Column(String(255), nullable=False, unique=True)

    posts = relationship("Post", secondary=post_keywords, back_populates="keywords")

    def __repr__(self):
        return f"Keyword(id={self.id}, word={self.word})"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    body = Column(String(255), nullable=False)
    post_id = Column(String(255), ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    post = relationship(Post, back_populates="comments")
    author = relationship(User, back_populates="comments")
    reactions = relationship(
        "Reaction", back_populates="comment", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"Comment(id={self.id}, body={self.body})"


class Reaction(Base):
    """This is 'like' same as it is in facebook but I didn't want to mix it with SQL keyword 'like' """

    __tablename__ = "reactions"
    __table_args__ = (
        CheckConstraint(
            "(post_id IS NULL OR comment_id IS NULL) AND NOT (post_id IS NULL AND comment_id IS NULL)"
        ),
    )

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    comment = relationship(Comment, back_populates="reactions")
    post = relationship(Post, back_populates="reactions")
    user = relationship(User, back_populates="reactions")

    def __repr__(self):
        return f"Reaction(id={self.id})"
