from flask import render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from . import main
from .. import db
from app.models import Book, User, Ten_Categories
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
    return render_template('index.html')

# @main.route('/<username>/books/')
@main.route('/books/')
def bookshelf():


    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    for book_instance in books:
        book_instance.classify_DDC = deweyDecimalLink(book_instance.isbn)
        book_instance.classify_ten_id = deweyToCategory(book_instance.classify_DDC)

    books_list = [book.serialize() for book in books]
    return jsonify(books_list)

@main.route('/books/categories')
def viewCategories():

    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    for book_instance in books:
        book_instance.classify_DDC = deweyDecimalLink(book_instance.isbn)
        book_instance.classify_ten_id = deweyToCategory(book_instance.classify_DDC)
        if book_instance.classify_ten_id is not None:
            category_obj = Ten_Categories.query.filter_by(classification=book_instance.classify_ten_id).first()
            category_obj.books.append(book_instance)
            # print(category_obj)


    books_within_categories = [category.to_json() for category in Ten_Categories.query.all()]
    return jsonify(books_within_categories)

@main.route('/books/upload', methods=['GET', 'POST'])
def csv_import():
    if request.method == 'POST':

        def book_init_func(row):
            book_instance = Book(row['title'])
            book_instance.author = row['author']
            book_instance.isbn = row['isbn']
            book_instance.isbn13 = row['isbn13']
        
            '''Dewey Number + Category'''        
            # book_instance.classify_DDC = deweyDecimalLink(book_instance.isbn)
            # book_instance.classify_ten_id = findTenCategory(book_instance.classify_DDC)
            
            '''Cleanup ISBN numbers'''        
            # book_instance.isbn = cleanISBN(book_instance.isbn)
            # book_instance.isbn13 = cleanISBN(book_instance.isbn13)

            '''Add rows to User.books'''        
            user = User.query.filter_by(username='john').first()
            user.books.append(book_instance)
        
            return book_instance

                     
        mapdict = {
            'Title' : 'title',
            'Author' : 'author',
            'ISBN' : 'isbn',
            'ISBN13' : 'isbn13',
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

    if isbn is None:
        return 'No ISBN'
    else:

        try:
            '''Classify API from ISBN -> JSON of book'''
            base = 'http://classify.oclc.org/classify2/Classify?'
            parmType = 'isbn'
            parmValue = isbn
            searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
                    
            
            xmlContent = urlopen(searchURL)
            xmlFile = xmlContent.read()
            xmlDict = xmltodict.parse(xmlFile)         
            jsonDumps = json.dumps(xmlDict)
            # with open (f'app/externalFiles/isbn-user-john.json', 'w') as f:
                # f.write(jsonDumps)
            jsonContentISBN = json.loads(jsonDumps)

        except AttributeError:
            jsonContentOWI = owiDewey(jsonContentISBN)
            isbnOWI = isbnDewey(jsonContentOWI)
            return isbnOWI
        
        try:
            isbnDirect = isbnDewey(jsonContentISBN)
            return isbnDirect

        except AttributeError:
            return 'int object has no attribute encode'


# '''Helper functions for above'''
# ---------------------------------------------------------

def isbnDewey(jsonContentISBN):

    if type(jsonContentISBN.get("classify").get('editions').get('edition')) == list:
        # return 'isbn to dewey in list form'
    

        try:
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
            return 'KeyError'
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
        

        except AttributeError:
            deweyNumber = 'missing'

    else:
        return "Key error"


    return deweyNumber

def owiDewey(jsonContentISBN):

    owi = jsonContentISBN.get("classify").get("works").get('work')[0].get('@owi')

    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType1 = 'owi'
    parmValue1 = owi
    searchURL = base + urlencode({parmType1:parmValue1.encode('utf-8')})


    '''redirect to OCLC's site to extract XML file of book'''
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonDumps = json.dumps(xmlDict)
    jsonContentOWI = json.loads(jsonDumps)

    return jsonContentOWI



def deweyToCategory(deweyNumber):
    '''Find the corresponding Category title'''

    firstNum = deweyNumber[0]
    for category in Ten_Categories.query.all():
        if firstNum == category.call_number[0]:
            return category.classification
        # return "no dewey number provided"




def cleanISBN(isbn):
    print(isbn)
    filterISBN = re.findall("[a-zA-Z0-9]", isbn)
    joinISBN = ('').join(filterISBN)

    return joinISBN


def addingFakeDewey(isbn):

    return 'testing fake dewey'


# -----------------------------------------------------------------------------------------------
# One time upload of categories

@main.route('/category/ten/upload', methods=['GET', 'POST'])
def csv_import_ten_categories():
    if request.method == 'POST':

        def category_init_func(row):
            category_instance = Ten_Categories()
            category_instance.call_number = row['call_number']
            category_instance.classification = row['classification']

            # category_instance = Ten_Categories_DDC(row['call_number'], row['classification'])
            return category_instance

                     
        mapdict = {
            'Call Number' : 'call_number',
            'Classification' : 'classification',
            }

        request.isave_to_database(
            field_name="file",
            session=db.session,
            table=Ten_Categories,
            initializer=category_init_func,
            mapdict=mapdict
        )      
          
        return redirect(url_for(".bookshelf", username='john'), code=302)

    return """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """



# --------------------------------------------------------------------
# Not using anymore
def findTenCategoryJson(deweyNumber):
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
        # 'm' : 'missing',
    }

    firstNum = deweyNumber[0]
    if firstNum not in deweyMapping:
        return 'not included'
    else:
        return deweyMapping[firstNum]
