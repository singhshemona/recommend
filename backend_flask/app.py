from flask import Flask, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Configs
# -----------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '4388cb0269cbe1d2a7c23dae8c64a9762f0838f63eed7f48'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Book=Book)



# Models
# -------------------------------------

from werkzeug.security import generate_password_hash, check_password_hash

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





# Routes
# -------------------------------
@app.route('/')
def index():
    return '<h1>Hello World</h1>'


@app.route('/bookshelf/', methods=['GET', 'POST'])
def bookshelf_user():
    # Lisa = User.query.filter_by(username='lisa').first()
    # all_books = Lisa.books.all()

    # return render_template('bookshelf.html', book=all_books)

    return '<h1>Book Shelf</h1>'