# from flask import Flask, render_template
# from flask_bootstrap import Bootstrap

# app = Flask(__name__)
# bootstrap = Bootstrap(app)

import os
from app import create_app, db
from app.models import User, Book
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Book=Book)


@app.cli.command()
def test():
    '''Run the unit tests'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)



'''
Routes - not including root
'''

@app.route('/bookshelf/', methods=['GET', 'POST'])
def bookshelf_user():
    # Lisa = User.query.filter_by(username='lisa').first()
    # all_books = Lisa.books.all()

    # return render_template('bookshelf.html', book=all_books)

    return '<h1>Book Shelf</h1>'