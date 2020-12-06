# from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, String, Sequence, text, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased, relationship

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
        return f"Addresses (email_address={self.email_address})"


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

print("\n")
print("JOIN STATEMENT")
print(session.query(User, Address).filter(User.id == Address.user_id).all())
# all parsuje do listy te wyniki
# Lepiej tak:
print(session.query(User, Address).join(Address).all())

# dodanie nowego adresu email dla usera id=4
new = Address(email_address='j25@yahoo.com', user_id=4)
session.add(new)
session.commit()

adalias1 = aliased(Address)
adalias2 = aliased(Address)

result = session.query(
    User.name,
    adalias1.email_address,
    adalias2.email_address,
) \
    .join(adalias1, User.addresses) \
    .join(adalias2, User.addresses) \
    .filter(adalias1.email_address == 'jack.doe@gmail.com') \
    .filter(adalias2.email_address == 'j25@yahoo.com')

for username, email1, email2 in result:
    print(username, email1, email2)

print("#####")

stmt = session.query(
    Address.user_id,
    func.count().label("address_count")
).group_by(Address.user_id).subquery()

# print(stmt)

query = session.query(User, stmt.c.address_count) \
    .outerjoin(stmt, User.id == stmt.c.user_id) \
    .group_by(User.id).all()
# bez metody subquery nie mozemy dostac się do stmt.c.address_count
# samo join pokaze TYLKO userow ktorzy faktycznie te adresy maja
# outer join nie wywali rekordow tych userów którzy nie maja adresow email, zamienione na none

for result in query:
    print(result)
