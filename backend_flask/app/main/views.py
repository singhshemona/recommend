from flask import render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from . import main
from .. import db
from app.models import Book, User
import flask_excel as excel
import xmltodict, json
from urllib.request import urlopen
from urllib.parse import urlencode
from json2table import convert
import json
import os
import re



@main.route('/')
def index():
    # return '<h1>Home Page</h1>'
    return render_template('index.html')

@main.route('/<username>/books/')
def bookshelf(username):


    user = User.query.filter_by(username=username).first()
    books = user.books.all()

    for book_instance in books:
        if book_instance.isbn:
            book_instance.classify_DDC = '23423424' #deweyDecimalLink(book_instance.isbn)


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

            '''Add rows to User.books'''        
            user = User.query.filter_by(username='john').first()
            user.books.append(book_instance)

            '''Cleanup ISBN numbers'''        
            # book_instance.isbn = cleanISBN(book_instance.isbn)
            # book_instance.isbn13 = cleanISBN(book_instance.isbn13)

            
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

        request.isave_to_database(
            field_name="file",
            session=db.session,
            table=Book,
            initializer=book_init_func,
            mapdict=mapdict
        )      
          
        return redirect(url_for(".bookshelf", username='john'), code=302) #redirect elsewhere

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




# isbn to Dewey decimal
@main.route('/dewey/', methods=["GET"])
def deweyDecimalLink(isbn):

    # user = User.query.filter_by(username='john').first()
    # sample_book = user.books[1]
    # isbn = sample_book.isbn

    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'isbn'
    parmValue = isbn
    searchURL = base + parmType + parmValue #urlencode({parmType:parmValue.encode('utf-8')})

        
    # redirect to OCLC's site to extract XML file of book
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonDumps = json.dumps(xmlDict)
    jsonContent = json.loads(jsonDumps)

    # items = jsonContent.get("classify").get('works').get('work')
    base = jsonContent.get("classify").get('editions').get('edition')[0]
    deweyNumber0 = base.get('classifications').get('class')[0].get('@sfa')
    deweyNumber1 = base.get('classifications').get('class')[1].get('@sfa')
    
    return jsonContent

    regexNumber0 = re.findall("[a-zA-Z]", deweyNumber0)
    regexNumber1 = re.findall("[a-zA-Z]", deweyNumber1)

    if len(regexNumber0) > 0:
        deweyNumber = deweyNumber1
    else:
        deweyNumber = deweyNumber0
    # pets_data = open("data.json", "w")
    # json.dump(xmlDict, pets_data)
    # pets_data.close()

    return deweyNumber


def cleanISBN(isbn):
    print(isbn)
    filterISBN = re.findall("[a-zA-Z0-9]", isbn)
    joinISBN = ('').join(filterISBN)

    return joinISBN