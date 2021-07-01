from flask import render_template
from . import main

@main.route('/')
def index():
    # return '<h1>Home Page</h1>'
    return render_template('index.html')



@main.route('/bookshelf/', methods=['GET', 'POST'])
def bookshelf_user():
    # Lisa = User.query.filter_by(username='lisa').first()
    # all_books = Lisa.books.all()

    # return render_template('bookshelf.html', book=all_books)

    return '<h1>Book Shelf</h1>'



