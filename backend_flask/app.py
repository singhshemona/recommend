from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)


class GoodReads_book(db.Model):
    __tablename__ = "goodreads_books"