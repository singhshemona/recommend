from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from flask_login import UserMixin

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
        # return f'<User: {self.username}>'  
        return '<User %r>' % self.username



class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # author_first = db.Column(db.String)
    # author_last = db.Column(db.String)
    classify_DDC = db.Column(db.Float)
    classify_category = db.Column(db.String)

    ''' Goodreads info from csv import '''
    book_id = db.Column(db.Integer)
    author = db.Column(db.String)
    additional_authors = db.Column(db.String)
    isbn = db.Column(db.String)
    isbn_13 = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    avg_rating = db.Column(db.Float)
    publisher = db.Column(db.String)
    binding = db.Column(db.String)
    pages = db.Column(db.Integer)
    year_publish = db.Column(db.Date) # Integeer?
    year_publish_original = db.Column(db.Date) # Integer?
    date_read = db.Column(db.Date)
    date_added = db.Column(db.Date)
    bookshelves = db.Column(db.String)






    def __repr__(self):
        # return f'<Book: {self.title}>'
        return '<Book %r>' % self.title
