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
    posts = relationship(
        "BlogPost", back_populates="author", lazy="dynamic"
    )

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
        back_populates="posts"
    )
    author = relationship(User, back_populates="posts")

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