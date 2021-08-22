from flask import request, redirect, url_for
from app.models import Book, User, Ten_Categories, Hundred_Categories, Thousand_Categories
from . import api
from .. import db
from .decorators import permission_required
import flask_excel as excel

import xmltodict, json
from urllib.request import urlopen
from urllib.parse import urlencode
import re



# Add ['DELETE'] method. Doesn't remove book info, only user association


# http://127.0.0.1:5000/api/v1/books/upload
@api.route('/books/upload', methods=['GET', 'POST'])
@permission_required(permission.WRITE)
def csv_import():
    if request.method == 'POST':

        def book_init_func(row):
            book_instance = Book(row['title'])
            book_instance.author = row['author']
            book_instance.isbn = row['isbn']
            book_instance.isbn13 = row['isbn13']
        
            
            
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
          
        '''Dewey Number + Category'''  
        user = User.query.filter_by(username='john').first()
        books = user.books.all()
        for book_instance in books:      
            book_instance.classify_DDC = deweyDecimalLink(book_instance.isbn) # 800
            book_instance.classify_ten_id = deweyToCategoryTen(book_instance.classify_DDC) # Literature          
            book_instance.classify_hundred_id = deweyToCategoryHundred(book_instance.classify_DDC) # Literature          
            book_instance.classify_thousand_id = deweyToCategoryThousand(book_instance.classify_DDC) # Literature          
            if book_instance.classify_ten_id is not None:
                category_obj = Ten_Categories.query.filter_by(id=book_instance.classify_ten_id).first()
                category_obj.books.append(book_instance)
                db.session.add(category_obj)
                db.session.commit()
            if book_instance.classify_hundred_id is not None:
                category_obj = Hundred_Categories.query.filter_by(id=book_instance.classify_hundred_id).first()
                category_obj.books.append(book_instance)
                db.session.add(category_obj)
                db.session.commit()
            if book_instance.classify_thousand_id is not None:
                category_obj = Thousand_Categories.query.filter_by(id=book_instance.classify_thousand_id).first()
                category_obj.books.append(book_instance)
                db.session.add(category_obj)
                db.session.commit()



            db.session.add(book_instance)
            db.session.commit()

        return redirect(url_for("main.viewBooks", username='john'), code=302) #redirect elsewhere

    return """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """

    # return render_template('bookshelf.html')


# # Most likely not use
# @api.route("/handson_view", methods=["GET"])
# def handson_table():
#     return excel.make_response_from_a_table(
#         session=db.session,
#         table=Book, 
#         file_type="handsontable.html"
#     )



# isbn to Dewey decimal
@api.route('/dewey/', methods=["GET"])
def deweyDecimalLink(isbn):

    # isbn = '1999683382'

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

            # return jsonContentISBN

        except AttributeError:
            jsonContentOWI = owiDewey(jsonContentISBN)
            isbnOWI = isbnDewey(jsonContentOWI)
            return isbnOWI
        # except UnboundLocalError:
        #     return "No jsonContentOWI"
        
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



def deweyToCategoryTen(deweyNumber):
    '''Find the corresponding Category title'''
    # deweyFloat = float(deweyNumber)
    firstNum_ten = deweyNumber[0]
    for category in Ten_Categories.query.all():
        if firstNum_ten == category.call_number[0]:
            return category.id

def deweyToCategoryHundred(deweyNumber):
    firstNum_hundred = deweyNumber[0:2]
    for category in Hundred_Categories.query.all():
        if firstNum_hundred == category.call_number[0:2]:
            return category.id

def deweyToCategoryThousand(deweyNumber):
    firstNum_thousand = deweyNumber[0:3]
    for category in Thousand_Categories.query.all():
        if firstNum_thousand == category.call_number[0:3]:
            return category.id
        # return "no dewey number provided"




def cleanISBN(isbn):
    print(isbn)
    filterISBN = re.findall("[a-zA-Z0-9]", isbn)
    joinISBN = ('').join(filterISBN)

    return joinISBN


def addingFakeDewey(isbn):

    return 'testing fake dewey'






errorValues = {

}