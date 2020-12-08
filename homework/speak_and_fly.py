from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Courses(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True)
    lessons = Column(Integer, nullable=False)
    description = Column(String(100))
    language_id = Column(Integer, ForeignKey("Languages.id"))
    category_id = Column(Integer, ForeignKey("Categories.id"))
    level_id = Column(Integer, ForeignKey("Levels.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    price = Column(Float)

    def __repr__(self):
        return f"Courses(id: {self.id}, lessons: {self.lessons}, description: {self.description}), " \
               f"language_id: {self.language_id}, category_id: {self.category_id}, level_id: {self.level_id} " \
               f"start_date: {self.start_date}, end_date: {self.end_date}, price: {self.price})"


class Languages(Base):
    __tablename__ = "Languages"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return f"Languages(id: {self.id}, name: {self.name})"


class Categories(Base):
    __tablename__ = "Categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return f"Categories(id: {self.id}, name: {self.name})"


class Levels(Base):
    __tablename__ = "Levels"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    description = Column(String(100))

    def __repr__(self):
        return f"Levels(id: {self.id}, name: {self.name}, description: {self.description})"


Base.metadata.create_all(engine)


def add_course(lesson, description, language_id, category_id, level_id, start_date, end_date, price):
    dt_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    dt_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    course = Courses(lessons=lesson, description=description, language_id=language_id, category_id=category_id,
                     level_id=level_id, start_date=dt_start_date, end_date=dt_end_date, price=price)

    session = Session()
    session.add(course)
    session.commit()


def add_language(name):
    language = Languages(name=name)

    session = Session()
    session.add(language)
    session.commit()


def add_category(name):
    category = Categories(name=name)

    session = Session()
    session.add(category)
    session.commit()


def add_levels(name, description):
    level = Levels(name=name, description=description)

    session = Session()
    session.add(level)
    session.commit()


add_course(20, "this is a fun course", 1, 2, 2, '2020-06-16', "2021-03-11", 766.5)

add_levels("A0", "A0 level course")
add_levels("A1", "A1 level course")
add_levels("A2", "A2 level course")
add_levels("B1", "B1 level course")
add_levels("B2", "B2 level course")
add_levels("C1", "C1 level course")
add_levels("C2", "C2 level course")

add_category("conventional course")
add_category("business course")
add_category("adult course")
add_category("children course")
add_category("exam course")

add_language("English")
add_language("German")
add_language("French")
add_language("Spanish")
add_language("Italian")

q = engine.execute('select price from Courses order by price desc').scalar()
print(q)

for course in session.query(Courses):
    print(course)

for course in session.query(Courses).filter(Courses.price <= 1000).filter(Courses.price >= 0):
    print(course)


# print(filter_by_price(500, 100))
