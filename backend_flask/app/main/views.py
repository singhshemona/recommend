from flask import render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
import flask_excel as excel
from . import main
from .. import db
from app.models import Book, User
import json

from .. import excel
from wrec import excel_doc


@main.route('/')
def index():
    # return '<h1>Home Page</h1>'
    return render_template('index.html')

@main.route('/<username>/books/')
def bookshelf(username):


    user = User.query.filter_by(username=username).first()
    books = user.books.all()

    books_list = [book.serialize() for book in books]
    return jsonify(books_list)

    # return render_template('bookshelf.html', books=books) #returns a list


@main.route('/books/upload', methods=['GET', 'POST'])
def csv_import():
    if request.method == 'POST':

        def book_init_func(row):
            book_instance = Book(row['title'])
            book_instance.book_id = row['book_id']
            book_instance.author = row['author']
            book_instance.additional_authors = row['additional_authors']
            book_instance.isbn = row['isbn']
            book_instance.isbn13 = row['isbn13']
            book_instance.my_rating = row['my_rating']
            book_instance.avg_rating = row['avg_rating']
            book_instance.publisher = row['publisher']
            book_instance.binding = row['binding']
            book_instance.pages = row['pages']
            book_instance.year_publish = row['year_published']
            book_instance.year_publish_original = row['year_publish_original']
            book_instance.date_read = row['date_read']
            book_instance.date_added = row['date_added']
            book_instance.bookshelves = row['bookshelves']
            return book_instance

        mapdict = {
            'Book Id' : 'book_id',
            'Title' : 'title',
            'Author' : 'author',
            'Additional Authors' : 'additional_authors',
            'ISBN' : 'isbn',
            'ISBN13' : 'isbn13',
            'My Rating' : 'my_rating',
            'Average Rating' : 'avg_rating',
            'Publisher' : 'publisher',
            'Binding' : 'binding',
            'Number of Pages' : 'pages',
            'Year Published' : 'year_published',
            'Original Publication Year' : 'year_publish_original',
            'Date Read' : 'date_read',
            'Date Added' : 'date_added',
            'Bookshelves' : 'bookshelves'        
            }

        # excel_request = excel.ExcelRequest('environ')
        excel.ExcelRequest.isave_to_database(
            field_name="file",
            session=db.session,
            table=Book,
            initializer=book_init_func,
            mapdict=mapdict
        )
        return redirect(url_for(".handson_table"), code=302) #redirect elsewhere
    return """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """

    # return render_template('bookshelf.html')


@main.route("/handson_view", methods=["GET"])
def handson_table():
    return excel.make_response_from_a_table(
        session=db.session,
        table=Book,
        file_type="handsontable.html"
    )



