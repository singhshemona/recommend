from werkzeug.security import generate_password_hash, check_password_hash
from . import db

bookshelf = db.Table('bookshelf', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    books = db.relationship('Book',
                            secondary=bookshelf,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.username}>'  
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_first = db.Column(db.String)
    author_last = db.Column(db.String)
    classify_DDC = db.Column(db.Float)
    classify_category = db.Column(db.String)

    def __repr__(self):
        return f'<Book: {self.title}>'
