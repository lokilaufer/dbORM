from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from models import Publisher, Book, Shop, Stock, Sale
import json

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship("Publisher")


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    id_shop = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer)
    book = relationship("Book")
    shop = relationship("Shop")


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date_sale = Column(Date)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer)
    stock = relationship("Stock")


engine = create_engine('postgresql://username:password@localhost/books_db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

publisher_identifier = input("Введите имя или айди издателя: ")


def get_shops(publisher_identifier):
    query = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale
    ).select_from(
        Shop
    ).join(
        Stock
    ).join(
        Book
    ).join(
        Publisher
    ).join(
        Sale
    )

    if publisher_identifier.isdigit():
        data = query.filter(Publisher.id == int(publisher_identifier)).all()
    else:
        publisher = session.query(Publisher).filter(Publisher.name == publisher_identifier).first()
        if publisher:
            data = query.filter(Publisher.id == publisher.id).all()
        else:
            data = None

    if data:
        for book_title, shop_name, price, date_sale in data:
            print(f"{book_title: <40} | {shop_name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")
    else:
        print("Издатель не найден")


get_shops(publisher_identifier)

session.close()
