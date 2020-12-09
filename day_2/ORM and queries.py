from sqlalchemy import create_engine, Column, Integer, String, Sequence, text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased


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

    def __repr__(self):
        return f"User(id: {self.id}, name: {self.name}, fullname: {self.fullname}, nickname: {self.nickname})"


Base.metadata.create_all(engine)

andrzej = User(name="Andrzej", fullname="Andrzej Gołota", nickname="Andżej")
janusz = User(name="Janusz", fullname="Janusz Tracz", nickname="prywaciarz")
mariusz = User(name="Mariusz", fullname="Mariusz Pudzianowski", nickname="Pudzian")

session.add_all([andrzej, janusz, mariusz])
session.commit()
q = engine.execute("SELECT * FROM users;").fetchall()

query = session.query(User) # sprawdzamy czy mamy jakichs userów w bazie danych

bob = User(name="Bob", fullname="Bobby Fisher", nickname="Chess genius/psycho")
session.add(bob)  # dodajemy boba do sesji
session.commit()  # commitujemy zmiany
bob.nickname = "Some nickname"
print(session.dirty)  # pokazanie zmodyfikowanych instancji, rekordów,
# wykrywa ze ta instancja odpowiadajaca zapisowi zostal zmieniony i nic sie ponziej z nim nie stalo
# dane obiektów ktore sa w sesji
print(session.query(User).all())  # mimo ze nie zapisalismy tego do bazy danych, to nam to query zwraca zmieniony nickname
# sesja sobie uwaza, ze skoro zmienilismy nickname to sobie go zapiszemy
# jezeli zmienimy dany obiekt, ktory byl zapisany do bazy danych, a nastepnie bedziemy robic query to to moze nas troszke przekamac
# dlatego wazne jest zeby pamietac o tych commitach
print(session.dirty)

print("\n")
print("MODYFIKACJA cd, session.new")
print(session.new)  # takie property, ktore ma zwroci obiekty nowe, w tym momencie nie ma zadnych
sam = User(name='Sam', fullname='Sam Smith', nickname='sam123')
session.add(sam)  # dodanie do sesji Sama, ale jeszcze bez commita
print(session.new)  # w identity secie pojawia sie obiekt sama
session.commit()  # zmiany commitowane
print(session.new)  # znowu pusty identity set

print("\n")
print("COFANIE SESJI")
print(session.query(User).all())  # wypisanie Userow
session.add(User(name='bob', fullname='Bob Marley', nickname='bobby'))
session.commit()  # zmiana commitowana
print(session.query(User).all())  # znowu wyszukanie Userow i jest ten bob
session.add(User(name='???', fullname='invalid', nickname='???'))  # dodanie kolejnego
print(session.query(User).all())  # w wynikach dwoch userow
session.rollback()
print(session.query(User).all())  # tutaj juz tylko bob, bez ???


print("\n")
print("ZAPYTANIA")
# for user in session.query(User):
#     print(user)
#
# for user in session.query(User).order_by(User.id):
#     print(user)

# for user in session.query(User).order_by(User.id.desc()):
#     print(user)

# for user in session.query(User).filter(User.id == 1):
#     print(user)
#
# for user in session.query(User).filter_by(id=1):
#     print(user)

# for user in session.query(User.id, User.nickname):
#     print(user)

# label - alias taki
for user in session.query(User.id, User.nickname.label('alter_ego')):
    print(user.id, user.alter_ego)


print("\n")
print("ZAPYTANIA - aliasy")
banned_users = aliased(User, name='banned_users')
for user in session.query(banned_users.nickname.label('alter_ego')):
    print(user.alter_ego)

print("\n")
print("ZAPYTANIA - generatywnosc")
andrzej = session.query(User).filter(User.id <= 2).filter(User.name == "Andrzej").one()
print(andrzej)

print("\n")
print("ZAPYTANIA - text")
user = session.query(User).filter(text("id=1")).one()
print(user)

print("\n")
print("ZAPYTANIA - statement")
statement = text("SELECT * from users WHERE id = :id")
statement = statement.columns(User.id, User.fullname, User.nickname)
user = session.query(User).from_statement(statement).params(id=1).one()
#wynik jest z 4 kolumn, a nie z 3, bo ten User jest tak jakby wazniejszy


session.query(func.count("*")).select_from(User).scalar()

print("\n")
print("ZAPYTANIA - grupowanie")
grouped_count = session.query(func.count(User.name), User.name).group_by(User.name).all()
for result in grouped_count:
    print(result)
# wszyscy userzy miei rozne umiona
# 1 - wynik zgrupowania, a nastepnie imie
# jakby dodac kogos o takim samym imieniu to byloby np 2 tam gdzie teraz 1




