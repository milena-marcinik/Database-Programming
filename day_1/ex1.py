from sqlalchemy import create_engine

# deifniujemy create engine
# connection string defiiniuje ze bedziemy korzystac z sqllite i bedziemy zapisywac do pamieci
# przy kazdym uruchomieniu pliku naszego ta baza danych od nowa sie robi
engine = create_engine("sqlite:///:memory:", echo=True)

employee = """
CREATE TABLE Employees(
id integer primary key autoincrement, 
first_name varchar(30) not null,
last_name varchar(30) not null,
position_id int not null,
salary_id int not null,
FOREIGN KEY (position_id) REFERENCES Positions(position_id),
FOREIGN KEY (salary_id) REFERENCES Salaries(salary_id));
"""

position = """
CREATE TABLE Positions(
id integer primary key autoincrement, 
name varchar(30) not null,
department_id int not null,
FOREIGN KEY (department_id) REFERENCES Departments(department_id));
"""

salary = """
CREATE TABLE Salaries(
id integer primary key autoincrement,
amount double not null
);
"""

department = """
CREATE TABLE Departments(
id integer primary key autoincrement, 
name varchar(30) not null,
manager varchar(30)
);
"""

# Creating tables
engine.execute(department)
engine.execute(salary)
engine.execute(position)
engine.execute(employee)


first_department = """
INSERT INTO Departments values (1, 'accounting', 'John Doe');
"""

engine.execute(first_department)
department_result = engine.execute("SELECT * from Departments;").fetchall()
print(department_result)

first_salary = """
INSERT INTO Salaries values (1, 1000.0);
"""

engine.execute(first_salary)

first_position = """
INSERT INTO Positions values (1, 'accountant', 1);
"""

engine.execute(first_position)

employee = """
INSERT INTO Employees values (1, 'John', 'Malkovich', 1, 1);
"""

engine.execute(employee)

get_employee = engine.execute("SELECT * from Employees;").fetchall()
print(get_employee)
