from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


# CREATE DATABASE


class Courses(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True)
    lessons_number = Column(Integer, nullable=False)
    description = Column(String(100))
    language_id = Column(Integer, ForeignKey("Languages.id"))
    category_id = Column(Integer, ForeignKey("Categories.id"))
    level_id = Column(Integer, ForeignKey("Levels.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    price = Column(Float)

    languages = relationship("Languages")
    categories = relationship("Categories")
    levels = relationship("Levels")

    def __repr__(self):
        return f"Courses(id: {self.id}, lessons_number: {self.lessons_number}, description: {self.description}), " \
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


# FUNCTIONS - add data to database


def add_course(lessons_number, description, language_id, category_id, level_id, start_date, end_date, price):
    dt_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    dt_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    course = Courses(lessons_number=lessons_number, description=description, language_id=language_id, category_id=category_id,
                     level_id=level_id, start_date=dt_start_date, end_date=dt_end_date, price=price)

    session.add(course)
    session.commit()


def add_language(name):
    language = Languages(name=name)

    session.add(language)
    session.commit()


def add_category(name):
    category = Categories(name=name)

    session.add(category)
    session.commit()


def add_levels(name, description):
    level = Levels(name=name, description=description)

    session.add(level)
    session.commit()


# ADD SAMPLE DATA (using functions)


levels = [("A0", "A0 level course"), ("A1", "A1 level course"), ("A2", "A2 level course"), ("B1", "B1 level course"),
          ("B2", "B2 level course"), ("C1", "C1 level course"), ("C2", "C2 level course")]

for level in levels:
    add_levels(level[0], level[1])


categories = ["conventional course", "business course", "adult course", "children course", "exam course"]

for category in categories:
    add_category(category)


languages = ["English", "German", "French", "Spanish", "Italian"]

for language in languages:
    add_language(language)


add_course(20, "this is a fun course", 1, 2, 2, '2020-06-16', "2021-03-11", 766.5)
add_course(28, "this is a fuuuuun course", 2, 1, 1, '2020-12-10', "2021-06-20", 1100)


# FUNCTIONS - return data from specific tables


def filter_by_price(min_price, max_price):
    filter_courses = []
    for course in session.query(Courses).filter(Courses.price > min_price, Courses.price < max_price).all():
        filter_courses.append(course)

    return filter_courses


def filter_by_language(language_name):
    filter_courses = []
    language_name = language_name.capitalize()
    subquery = session.query(Languages.id).filter(Languages.name == language_name).subquery()

    for course in session.query(Courses).filter(Courses.id.in_(subquery)):
        filter_courses.append(course)

    return filter_courses


# print(filter_by_language("german"))
