import json
from typing import List, Annotated, Set, Dict

from sqlalchemy import create_engine, String, ForeignKey, select, or_, and_, insert, delete, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, attribute_keyed_dict, \
    joinedload, subqueryload

sql_engine = create_engine(f"mysql+pymysql://root:@127.0.0.1/testdb", echo=True)
SessionLocal = sessionmaker(autocommit=False, bind=sql_engine)


str_50 = Annotated[str, 50]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_50: String(50)
    }

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[str_50] = mapped_column(primary_key= True, autoincrement=False)
    name: Mapped[str_50]
    books: Mapped[List["Book"]] = relationship(back_populates="author", order_by="-Book.title")
#map    books: Mapped[Dict[str, "Book"]] = relationship(back_populates="author", collection_class=attribute_keyed_dict("id"))


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[str_50] = mapped_column(primary_key= True)
    title: Mapped[str_50]

    author_id: Mapped[str_50] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Author] = relationship(back_populates="books")

##   Case for mapping without foreign key
# class Author(Base):
#     __tablename__ = 'authors'
#
#     id: Mapped[str_50] = mapped_column(primary_key= True)
#     name: Mapped[str_50]
#     books: Mapped[List["Book"]] = relationship(primaryjoin="foreign(Author.id) == Book.author_id",
# #map    books: Mapped[Dict[str, "Book"]] = relationship(primaryjoin="foreign(Author.id) == Book.author_id",
#                                                back_populates="author",
#                                                order_by="-Book.title",
# #map                                               collection_class=attribute_keyed_dict("id"),
#                                                uselist=True)
#
# class Book(Base):
#     __tablename__ = 'books'
#
#     id: Mapped[str_50] = mapped_column(primary_key= True)
#     title: Mapped[str_50]
#
#     author_id: Mapped[str_50] = mapped_column()
#     author = relationship("Author",
#                           primaryjoin="foreign(Book.author_id) == Author.id")

Base.metadata.create_all(sql_engine)

# with SessionLocal() as session:
#     author = Author(id='1', name="J.K. Rowling")
#     book1 = Book(id='100', title="Harry Potter and the Philosopher's Stone", author_id="1")
#     book2 = Book(id='101',title="Harry Potter and the Chamber of Secrets", author_id="1")
#     book3 = Book(id='103', title="Harry Potter and Prisoner of Azkaban", author_id="1")
#
#     author2 = Author(id='2', name="George Orwell")
#     book3 = Book(id='200',title="1984", author_id="2")
#     book4 = Book(id='201',title="Animal Farm", author_id="2")
#
#     session.add_all([author, book1, book2, author2, book3, book4])
#     session.commit()

# with SessionLocal() as session:
#     author = session.get(Author, '1')
#     book2_2 = Book(id='104',title="Harry Potter and the Goblet of Fire", author=author)
#     author.books.append(book2_2)
#     session.add(book2_2)
#     session.commit()


with SessionLocal() as session:
    author = session.get(Author, '1')
    print(f"Author: {author.name}")
    for book in author.books:
        print(f"  Book: {book.title} - {book.id}")
#map    for key, book in author.books.items():
#map        print(f"  Book: {book.title} - {key}")


a1 = None
with SessionLocal() as session:
    session.expire_on_commit = False
    a1 = session.get(Author, '1')
    for book in a1.books:
        pass
    session.commit()

print(f"Author: {a1.name}")
for book in a1.books:
    print(f"  Book: {book.title}")


with SessionLocal() as session:
    stmt = select(Author)
    result = session.execute(stmt).all()
    for row in result:
        print(f"Author: {row[0].__dict__}")


with SessionLocal() as session:
    stmt = select(Author)
    result = session.scalars(stmt.where(Author.name.like("%J.%"))).all()
    for row in result:
        print(f"Author: {row.__dict__}")

    stmt = select(Author, Book)
    result = session.execute(stmt).all()
    for row in result:
        print(f"Result: {row[0].__dict__}, {row[1].__dict__}")

    stmt = select(Book.title, Author.name).join(Book.author)
    result = session.execute(stmt).all()
    for row in result:
        print(f"Result columns: {row[0]} - {row[1]}")

with SessionLocal() as session:
    session.execute(insert(Book), [
        {'id': '105', 'title': 'Harry Potter and Half-Blood Prince', 'author_id': '1'},
        {'id': '106', 'title': 'Harry Potter and Deathly Hallows', 'author_id': '1'}
    ])
    stmt = select(Author, Book)
    result = session.execute(stmt).all()
    for row in result:
        print(f"Result: {row[0].__dict__}, {row[1].__dict__}")
    session.rollback()

# with SessionLocal() as session:
#     book4 = Book(id='105', title='Harry Potter and Half-Blood Prince', author_id='1')
#     session.add(book4)
#     book3 = session.get(Book, '103')
#     book3.title = '3. ' + book3.title
#     session.execute(delete(Book).where(Book.id == '105'))
#     session.execute(update(Book).where(Book.id == '103').values(title='III. Harry Potter and Prisoner of Azkaban'))
#
#     result = session.execute(select(Book)).all()
#     for row in result:
#         print(f"Result: {row[0].__dict__}")
#     session.commit()
#
# with SessionLocal() as session:
#     result = session.scalars(select(Book)).all()
#     for row in result:
#         print(f"Result: {row.__dict__}")

with SessionLocal() as session:
    result = session.scalars(select(Author).options(joinedload(Author.books))).unique()
    for row in result:
        print(f"Result: {row.__dict__}")

with SessionLocal() as session:
    result = session.scalars(select(Author).options(subqueryload(Author.books))).all()
    for row in result:
        print(f"Result: {row.__dict__}")

