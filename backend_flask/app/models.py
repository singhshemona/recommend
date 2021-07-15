from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from flask_login import UserMixin
from flask_serialize import FlaskSerializeMixin


bookshelf = db.Table('bookshelf', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Book',
                            secondary=bookshelf,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)

    ''' Classify API + DDC Table '''
    classify_DDC = db.Column(db.String)
    classify_category = db.Column(db.String) # replace later with 3 other tables
    classify_ten_id = db.Column(db.String, db.ForeignKey('ten_categories_DDC.id'))

    ''' Goodreads info from csv import '''
    book_id = db.Column(db.String)
    title = db.Column(db.String)
    author = db.Column(db.String)
    additional_authors = db.Column(db.String)
    isbn = db.Column(db.String)
    isbn13 = db.Column(db.String)
    my_rating = db.Column(db.Integer)
    avg_rating = db.Column(db.Float)
    publisher = db.Column(db.String)
    binding = db.Column(db.String)
    pages = db.Column(db.Integer)
    year_publish = db.Column(db.String) # Integer?
    year_publish_original = db.Column(db.String) # Integer?
    date_read = db.Column(db.String) # Datetime.date?
    date_added = db.Column(db.String) # Datetime.date?
    bookshelves = db.Column(db.String)


    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Book %r>' % self.title

    def serialize(self):
        book_user = {
            'title' : self.title,
            'author' : self.author,
            'classify_DDC' : self.classify_DDC,
            'classify_category' : self.classify_category,
            'isbn' : self.isbn,
            'isbn13' : self.isbn13
        }
        return book_user


class Ten_Categories_DDC(db.Model):
    __tablename__ = 'ten_categories_DDC'
    id = db.Column(db.Integer, primary_key=True)
    call_number = db.Column(db.String)
    classification = db.Column(db.String)
    books = db.relationship('Book', backref='classify_ten')