from sqlalchemy import func, text
from sqlalchemy.orm import sessionmaker, aliased

from homework_blog_post.data import USERS, POSTS, COMMENTS, REACTIONS
from homework_blog_post.models import User, engine, Base, Post, Comment, Reaction

Session = sessionmaker(bind=engine)
session: Session = Session()
Base.metadata.create_all(bind=engine)


def create_users(data):
    user_objs = [User(**user_data) for user_data in data]
    session.add_all(user_objs)
    session.commit()


def create_posts(data):
    post_objs = [Post(**post_data) for post_data in data]
    session.add_all(post_objs)
    session.commit()


def create_comments(data):
    comment_objs = [Comment(**comment_data) for comment_data in data]
    session.add_all(comment_objs)
    session.commit()


def create_reactions(data):
    reaction_objs = [Reaction(**reaction_data) for reaction_data in data]
    session.add_all(reaction_objs)
    session.commit()


def create_data():
    create_users(USERS)
    create_posts(POSTS)
    create_comments(COMMENTS)
    create_reactions(REACTIONS)


if __name__ == "__main__":
    create_data()

"""
-1 Query które zwróci najbardziej komentowany post
-2 Query które zwróci najbardziej lajkowany post
-3 Query które zwróci najbardziej lajkowany komentarz
-4 Query które zwróci usera który dostał najwięcej lajków
-5 Query które zwróci usera z największą liczbą postów
-6 Query które zwróci usera z największa liczbą komentarzy
-7 Na podstawie tego jak były robione dane z innych tabel, zrobić 'fixtury' dla keywords
-8 Zwrócić post który ma najwięcej liter 'a'
-9 Zwrócić komentarze które zaczynają się na 'a' (niezależnie od wielkości liter)
"""
# 1 Query które zwróci najbardziej komentowany post
q1 = (
    session.query(Post, func.count(Comment.id).label("comment_count"))
        .join(Comment, Comment.user_id == Post.id)
        .group_by(Comment.post_id)
        .order_by(text("comment_count DESC"))
        .first()
)

stmt1 = (
    session.query(Comment, func.count(Comment.id).label("comment_count"))
        .group_by(Comment.post_id)
        .subquery()
)
q1_1 = (
    session.query(Post, stmt1.c.comment_count)
        .join(Post, Post.id == stmt1.c.post_id)
        .order_by(stmt1.c.comment_count.desc())
        .first()
)

# 2 Query które zwróci najbardziej lajkowany post
stmt2 = (
    session.query(Reaction, func.count(Reaction.id).label("reaction_count"))
        .group_by(Reaction.post_id)
        .subquery()
)

q2 = (
    session.query(Post, stmt2.c.reaction_count)
        .join(Post, Post.id == stmt2.c.post_id)
        .order_by(stmt2.c.reaction_count.desc())
        .first()
)

# 3 Query które zwróci najbardziej lajkowany komentarz
stmt3 = (
    session.query(Reaction, func.count(Reaction.id).label("reaction_count"))
        .group_by(Reaction.comment_id)
        .subquery()
)

q3 = (
    session.query(Comment, func.max(stmt3.c.reaction_count))
        .join(Comment, Comment.id == stmt3.c.comment_id)
        .one()
)

# 4 Query które zwróci usera który dostał najwięcej lajków
stm4 = (
    session.query(Reaction, func.count(Reaction.id).label("reaction_count"))
        .group_by(Reaction.post_id, Reaction.comment_id)
        .subquery()
)

alias_comment = aliased(User)
alias_post = aliased(User)

q4 = (
    session.query(alias_comment, alias_post, func.max(stm4.c.reaction_count))
        .join(alias_comment, alias_comment.id == stm4.c.comment_id)
        .join(alias_post, alias_post.id == stm4.c.post_id)
        .one()
)

# 5 Query które zwróci usera z największą liczbą postów
stmt5 = (
    session.query(Post, func.count(Post.id).label("post_count"))
        .group_by(Post.user_id)
        .subquery()
)

q5 = (
    session.query(User, func.max(stmt5.c.post_count))
        .join(User, User.id == stmt5.c.user_id)
        .one()
)

# 6 Query które zwróci usera z największa liczbą komentarzy
stmt6 = (
    session.query(Comment, func.count(Comment.id).label("comment_count"))
        .group_by(Comment.user_id)
        .subquery()
)

q6 = (
    session.query(User, func.max(stmt6.c.comment_count))
        .join(User, User.id == stmt6.c.user_id)
        .one()
)

# 8 Zwrócić post który ma najwięcej liter 'a'

length_post = func.length(Post.body)
length_post_without_a = func.length(func.replace(Post.body, "a", ""))

q8 = (session.query(Post, func.min(length_post - length_post_without_a).label("count_letter_a"))
      .group_by(Post.id)
      .order_by(text("count_letter_a desc"))
      .first())

# 9 Zwrócić komentarze które zaczynają się na 'a' (niezależnie od wielkości liter)
q9 = (session.query(Comment).filter(Comment.body.ilike("a%")).all())

print(f"1: Query które zwróci najbardziej komentowany post: {q1}")
print(f"1: Query które zwróci najbardziej komentowany post:{q1_1}")
print(f"2: Query które zwróci najbardziej lajkowany post: {q2}")
print(f"3: Query które zwróci najbardziej lajkowany komentarz: {q3}")
print(f"4: Query które zwróci usera który dostał najwięcej lajków: {q4}")
print(f"5: Query które zwróci usera z największą liczbą postów: {q5}")
print(f"6: Query które zwróci usera z największa liczbą komentarzy: {q6}")
print("7")
print(f"8: Zwrócić post który ma najwięcej liter 'a': {q8}")
print(f"9: Zwrócić komentarze które zaczynają się na 'a': {q9}")
