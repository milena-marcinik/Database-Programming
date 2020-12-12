from sqlalchemy import create_engine, Column, Integer, String, Sequence, text, func, ForeignKey, exists, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased, relationship, selectinload, joinedload, contains_eager

engine = create_engine("sqlite:///:memory:", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    addresses = relationship("Address", order_by="Address.id", back_populates="user",
                             cascade="all, delete, delete-orphan")

    posts = relationship("BlogPost", back_populates="author", lazy="dynamic")

    def __repr__(self):
        return f"User(id: {self.id}, name: {self.name}, fullname: {self.fullname}, nickname: {self.nickname})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Addresses (email_address={self.email_address})"


# association table
print("ASSOCIATION TABLE")
post_keywords = Table("post_keywords", Base.metadata,
                      Column("post_id", ForeignKey("posts.id"), primary_key=True),
                      Column("keyword_id", ForeignKey("keywords.id"), primary_key=True)
                      )


# table jest konstruktorem
# kazda kolejna koumna jets przekazana jako argument


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
        

Base.metadata.create_all(engine)

andrzej = User(name="Andrzej", fullname="Andrzej Gołota", nickname="Andżej")
janusz = User(name="Janusz", fullname="Janusz Tracz", nickname="prywaciarz")
mariusz = User(name="Mariusz", fullname="Mariusz Pudzianowski", nickname="Pudzian")

session.add_all([andrzej, janusz, mariusz])
session.commit()
q = engine.execute("SELECT * FROM users;").fetchall()

jack = User(name='Jack', fullname='Jack Doe', nickname='jc123')
print(jack.addresses)
jack.addresses = [Address(email_address='jack.doe@gmail.com')]
print(jack.addresses)
print(jack.addresses[0].user)

session.add(jack)
session.commit()

new = Address(email_address='j25@yahoo.com', user_id=4)
session.add(new)
session.commit()


print("RELACJA WIELU DO WIELU")
post = BlogPost("Jack's first post", "Hello world", jack)
session.add(post)
session.commit()

post.keywords.append(Keyword("jack"))
post.keywords.append(Keyword("world"))
session.commit()

# wyszukanie postów ze slowem kluczowym "world"
keyword_filter = BlogPost.keywords.any(keyword="world")
print(session.query(BlogPost).filter(keyword_filter).all())

# z autorem Jackiem i slowem "world"
print(session.query(BlogPost).filter(BlogPost.author==jack).filter(keyword_filter).all())
# lub
print(jack.posts.filter(keyword_filter).all())
