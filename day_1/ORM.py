from sqlalchemy import create_engine, Integer, String, Column, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # fabryka, ktora tworzy klase, w my jeszcze z tej klasy bedziemy robic instancje sesji i na niej pracowac

engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    def __repr__(self):
        return f"User(id: {self.id}, name: {self.name}, fullname: {self.fullname})"


# wazne zeby byla pod klasa ta metoda, wszystkie tabele zadeklarowane nad nią ona stworzy
Base.metadata.create_all(engine) # ten engine to jest konkretny engine z którego korzystamy
# jak korzystamy z jednej bazy danych to najlepiej zeby tylko jeden engine byl

edward = User(name='Ed', fullname='Edward Jones', nickname='big_daddy')
print(edward.id) # znaim to dostaniemy, to musimy zapisac obiekt w bazie danych, w tym momencie tylko instancja klasy User


session = Session()  # bedziemy na instancji dzialac
session.add(edward)
session.commit()

q = engine.execute('select * from users').fetchall()
print(q)

session.add_all([
    User(name='Sam', fullname='Sam More', nickname='sammy12'),
    User(name='Joe', fullname='Joe Smith', nickname='js21')
])
session.commit()  # zatwierdza zmiany
q = engine.execute('select * from users').fetchall()
print(q)

query = session.query(User)
# to ponizej trzeba pojedynczo printować
print(query.all())
# query.one() on nie wyrzuci bledu tylko wtedy jak bedzie jeden obiekt w tym query
# query.scalar()
# query.scalar()


print("MODYFIKACJA REKORDU WCZEŚNIEJ DODANEGO DO SESJI")
session.query(User).all()
bob = User(name='Bob', fullname='Bob Marley', nickname='bobby')
session.add(bob)
session.commit()
bob.nickname = 'bobby42'  # ten bob to jest instancja klasy User, mozemy dynamicznie te atrybuty zmieniac
print(session.dirty)  # pokazuje cos, jak cos robilismy nie nie dalismy ani query ani commita
print(session.query(User).all())
print(session.dirty)  # tu nic nie ma, jest cos takiego jak flash, taki mechanizm, taki git add, session commit to jest jak zapisanie commita w repo
# sql alchemy dziala tak, ze przy kazdym zapytaniu query nastepuje taki autoflash
# czyli automatycznie ta nasza instancja, która zmienilismy i zmiana nie zostala zacommitowana, została "przekazana" na taki staging w gicie
# dlatego tez ona pozniej nie wyswietla sie jako dirty
