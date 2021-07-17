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
        # print(book_instance.id, book_instance.title)
        if book_instance.isbn is None:
            continue
        else:
            deweyNumberBook = deweyDecimalLink(book_instance.isbn)
            book_instance.classify_DDC = deweyNumberBook
            # db.session.add(deweyNumberBook.classify_DDC)

            tenCategory = findTenCategory(book_instance.classify_DDC)
            book_instance.classify_ten_id = tenCategory
            # db.session.add(tenCategory)

            # db.session.commit()


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
    # sample_book = user.books.filter_by(id=60).first() # The Library Book
    # print(sample_book.title)

    # isbn = sample_book.isbn






    # for book in user.books:
    #     print(book.id)
    #     if book.isbn is None:
    #         continue
    #     else:
    #         isbn = book.isbn

    # # sample_book = user.books[35]
    # isbn13 = sample_book.isbn13




    '''Classify API from ISBN -> JSON of book'''
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'isbn'
    parmValue = isbn
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})

            
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonDumps = json.dumps(xmlDict)
    jsonContentISBN = json.loads(jsonDumps)

    # return jsonContentISBN
    # if jsonContentISBN.get("classify"):
    #     base = jsonContentISBN.get("classify")
    #     bookList.append(base)
    # else:
    #     empty = []
    #     bookList.append(empty)

    # try:
    try:
        # base = jsonContentISBN.get("classify").get('editions').get('edition')[0]

        isbnDirect = isbnDewey(jsonContentISBN)

        # bookList.append(isbnDirect) 
        # print(isbnDirect)
        return isbnDirect
    except AttributeError:
        # return jsonContentISBN
        jsonContentOWI = owiDewey(jsonContentISBN)
        # return jsonContentOWI
        isbnOWI = isbnDewey(jsonContentOWI)
        # bookList.append(isbnOWI)
        # print(isbnOWI)
        return isbnOWI

    # print(bookList)    
    # return jsonify(bookList)

    


'''Helper functions for above'''
def isbnDewey(jsonContentISBN):
    
    # return jsonContentISBN
    # return base
        # print('True')
        # return str('Not a list')
        
    # else:
        # print('False')
        # return str('False')

    
    try:
        # jsonContentISBN.get("classify").get('editions').get('edition')[0]:
        base = jsonContentISBN.get("classify").get('editions').get('edition')[0]
        # try:
        deweyNumber0 = base.get('classifications').get('class')[0].get('@sfa')
        deweyNumber1 = base.get('classifications').get('class')[1].get('@sfa')

        regexNumber0 = re.findall("[a-zA-Z]", deweyNumber0)
        regexNumber1 = re.findall("[a-zA-Z]", deweyNumber1)

        if len(regexNumber0) > 0:
            deweyNumber = deweyNumber1
        else:
            deweyNumber = deweyNumber0

    except KeyError:
        try:
            base = jsonContentISBN.get("classify").get('editions').get('edition')[0]
            deweyNumber = base.get('classifications').get('class').get('@sfa')
        except KeyError:
            base =  jsonContentISBN.get("classify").get('editions').get('edition')
            deweyNumber0 = base.get('classifications').get('class')[0].get('@sfa')
            deweyNumber1 = base.get('classifications').get('class')[1].get('@sfa')

            regexNumber0 = re.findall("[a-zA-Z]", deweyNumber0)
            regexNumber1 = re.findall("[a-zA-Z]", deweyNumber1)

            if len(regexNumber0) > 0:
                deweyNumber = deweyNumber1
            else:
                deweyNumber = deweyNumber0

        
        # deweyNumber = '1234567890'
        # return deweyNumber

    except AttributeError:
        deweyNumber = 'missing'

    # else:

    # elif base.get('classifications').get('class'):
        # deweyNumber = base.
        
        # try:

        # except:
    # else:
        # return jsonify(base.get('classifications').get('class'))
            # deweyNumber = base.get('classifications').get('class').get('@sfa')
        

        # pets_data = open("data.json", "w")
        # json.dump(xmlDict, pets_data)
        # pets_data.close()


    return deweyNumber

def owiDewey(jsonContentISBN):

    # return jsonContentISBN
    # print('owi to dewey')
    owi = jsonContentISBN.get("classify").get("works").get('work')[0].get('@owi')


    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType1 = 'owi'
    parmValue1 = owi
    searchURL = base + urlencode({parmType1:parmValue1.encode('utf-8')})


    # redirect to OCLC's site to extract XML file of book
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonDumps = json.dumps(xmlDict)
    jsonContentOWI = json.loads(jsonDumps)

    return jsonContentOWI

def findTenCategory(deweyNumber):
    deweyMapping = {
        '0' : 'Computer science, information & general works',
        '1' : 'Philosophy & psychology',
        '2' : 'Religion',
        '3' : 'Social sciences',
        '4' : 'Language',
        '5' : 'Science',
        '6' : 'Technology',
        '7' : 'Arts & recreation',
        '8' : 'Literature',
        '9' : 'History & geography',
        'm' : 'missing',
    }

    firstNum = deweyNumber[0]
    if firstNum not in deweyMapping:
        return 'not included'
    else:
        return deweyMapping[firstNum]






def cleanISBN(isbn):
    print(isbn)
    filterISBN = re.findall("[a-zA-Z0-9]", isbn)
    joinISBN = ('').join(filterISBN)

    return joinISBN