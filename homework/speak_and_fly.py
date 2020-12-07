from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Courses(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True)
    lessons = Column(Integer, nullable=False)
    description = Column(String(100))
    language_id = Column(Integer, ForeignKey("Languages.id"))
    category_id = Column(Integer, ForeignKey("Categories.id"))
    level_id = Column(Integer, ForeignKey("Levels.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    price = Column(Float)

    def __repr__(self):
        f"Courses(id: {self.id}, lessons: {self.lessons}, description: {self.description}), " \
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