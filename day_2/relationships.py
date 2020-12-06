# from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, String, Sequence, text, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased, relationship


engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    addresses = relationship("Address", order_by="Address.id", back_populates="user")

    def __repr__(self):
        return f"User(id: {self.id}, name: {self.name}, fullname: {self.fullname}, nickname: {self.nickname})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Addresses (email_address={self.email_addresses})"


Base.metadata.create_all(engine)

andrzej = User(name="Andrzej", fullname="Andrzej Gołota", nickname="Andżej")
janusz = User(name="Janusz", fullname="Janusz Tracz", nickname="prywaciarz")
mariusz = User(name="Mariusz", fullname="Mariusz Pudzianowski", nickname="Pudzian")

session.add_all([andrzej, janusz, mariusz])
session.commit()
q = engine.execute("SELECT * FROM users;").fetchall()
