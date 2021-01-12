from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:", echo=True)

query = engine.execute("CREATE TABLE Users(id int, name varchar, nickname varchar)")
print(query)

users = [
    (1, "Roman", "magneton_bora"),
    (2, "Sam", "big_daddy"),
    (3, "Sara", "lovely_kitty"),
]

# breakpoint() i potem mozna w terminalu w pdb wpisać np "users" i sprawdzic czym są


def add_users(engine, users):
    results = []
    for (user_id, name, nick) in users:
        insert_into = engine.execute(
            f"INSERT INTO Users values('{user_id}', '{name}', '{nick}')"
        )
        results.append(insert_into)
    return results


for result in add_users(engine, users):
    print(result)

# do zmiennej result przypisane zapytanie które zwraca wszystkich userow
result = engine.execute("SELECT * from Users").fetchall()  #fetchall - do listy tupli parsuje te wyniki, "resultset"
# samo engine.execute daje ten obiekt result proxy, po tym tez moglibysmy iterowac
# głównym obiektem bedzie query i na tym bedzimey dzialali filtrujac sobie dane czy wyciagajac
# jak bedziemy chcieli cos wyciagac to beda metody takie jak all, które beda ulatwialy wypisywanie tych danych

for user in result:
    print(f"{user.id}, {user.name}, {user.nickname}")

