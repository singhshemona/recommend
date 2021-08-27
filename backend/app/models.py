from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from flask_login import UserMixin
from flask_serialize import FlaskSerializeMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


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

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                        expires_in=expiration)
        return s.dumps({'id' : self.id}).decode('utf-8')
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username

    def circle_packing(self):
        ten_cat = Ten_Categories.query.all()
        ten_cat_list = [ten_category.classification for ten_category in ten_cat]

        hun_cat = Hundred_Categories.query.all()
        hun_cat_list = [hun_category.classification for hun_category in hun_cat]

        thou_cat = Thousand_Categories.query.all()
        thou_cat_list = [thou_category.classification for thou_category in thou_cat]


        bookshelf_circle = [
            {
                "name" : "books",
                "children" : [
                ],
            }
        ]
        return bookshelf_circle




class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)

    ''' Classify API + DDC Table '''
    classify_ddc = db.Column(db.String)
    classify_category = db.Column(db.String) # replace later with 3 other tables
    classify_ten_id = db.Column(db.Integer, db.ForeignKey('ten_categories_ddc.id')) # All 3 below were strings, forced to convert
    classify_hundred_id = db.Column(db.Integer, db.ForeignKey('hundred_categories_ddc.id'))
    classify_thousand_id = db.Column(db.Integer, db.ForeignKey('thousand_categories_ddc.id'))

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
            'classify_DDC' : self.classify_ddc,
            'classify_ten_id' : self.classify_ten_id,
            'classify_hundred_id' : self.classify_hundred_id,
            'classify_thousand_id' : self.classify_thousand_id,
            'isbn' : self.isbn,
            'isbn13' : self.isbn13
        }
        return book_user




class Ten_Categories(db.Model):
    __tablename__ = 'ten_categories_ddc'
    id = db.Column(db.Integer, primary_key=True)
    call_number = db.Column(db.String) # Should be a different data type
    classification = db.Column(db.String)
    hundred_values = db.relationship('Hundred_Categories', backref='hundred_ten_categories')
    books = db.relationship('Book', backref='classify_ten')




    def to_json(self):
        books = {
            'call_number' : self.call_number,
            'classification' : self.classification,
            'books' : [book.title for book in self.books]
        }
        return books




class Hundred_Categories(db.Model):
    __tablename__ = 'hundred_categories_ddc'
    id = db.Column(db.Integer, primary_key=True)
    call_number = db.Column(db.String)
    classification = db.Column(db.String)
    tens_id = db.Column(db.Integer, db.ForeignKey('ten_categories_ddc.id'))
    thousand_values = db.relationship('Thousand_Categories', backref='thousand_ten_categories')
    books = db.relationship('Book', backref='classify_hundred')

    

    
    
    def to_json(self):
        books = {
            'call_number' : self.call_number,
            'classification' : self.classification,
            'books' : [book.title for book in self.books]
        }
        return books

class Thousand_Categories(db.Model):
    __tablename__ = 'thousand_categories_ddc'
    id = db.Column(db.Integer, primary_key=True)
    call_number = db.Column(db.String)
    classification = db.Column(db.String)
    hundreds_id = db.Column(db.Integer, db.ForeignKey('hundred_categories_ddc.id'))
    books = db.relationship('Book', backref='classify_thousand')


    def to_json(self):
        books = {
            'call_number' : self.call_number,
            'classification' : self.classification,
            'books' : [book.title for book in self.books]
        }
        return books


