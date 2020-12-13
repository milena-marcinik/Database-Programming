from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, Sequence, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("sqlite:///:memory:", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# association table
print("ASSOCIATION TABLE")
post_keywords = Table("post_keywords", Base.metadata,
                      Column("post_id", ForeignKey("posts.id"), primary_key=True),
                      Column("keyword_id", ForeignKey("keywords.id"), primary_key=True)
                      )


# table jest konstruktorem
# kazda kolejna koumna jets przekazana jako argument


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    posts = relationship("BlogPost", back_populates="author", lazy="dynamic")
    comments = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"User(id: {self.id}, name: {self.name})"


class BlogPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # konieczność istnienia i wskazania parametru secondary = w nim obiekt Table reprezentujacy tabelke laczaca
    # ta tabela sklada się z dwoch kolumn - po jednej odpowiadajacej kazdej ze stron relacji
    keywords = relationship(
        "Keyword",
        secondary=post_keywords,
        back_populates="posts",
    )
    author = relationship(User, back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return f"BlogPost({self.headline}, {self.body}, {self.author})"


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)

    posts = relationship(
        "BlogPost",
        secondary=post_keywords,
        back_populates="keywords"
    )

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return f"Keyword({self.id}, {self.keyword})"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    title = Column(String(40))
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    post = relationship("BlogPost", back_populates="comments")
    author = relationship("User", back_populates="comments")
    # reactions = relationship("Reaction", back_populates="comments")

    def __repr__(self):
        return f"Comment(id: {self.id}, author: {self.author})"


Base.metadata.create_all(engine)


jack = User(name='Jack', fullname='Jack Doe', nickname='jc123')
session.add(jack)
session.commit()

post = BlogPost("Jack's first post", "Hello world", jack)
session.add(post)
session.commit()

post.keywords.append(Keyword("jack"))
post.keywords.append(Keyword("world"))
session.commit()

print(session.query(User).first())
print(session.query(BlogPost).all())
print(session.query(Keyword).all())

keyword_filter = BlogPost.keywords.any(keyword="world")
print(session.query(BlogPost).filter(keyword_filter).all())
