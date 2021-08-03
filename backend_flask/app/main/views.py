from flask import render_template, jsonify, request, url_for, redirect
from . import main
from .. import db
from app.models import Book, User, Ten_Categories, Hundred_Categories, Thousand_Categories
from ..api.books import deweyDecimalLink, deweyToCategory


@main.route('/')
def index():
    return render_template('index.html')

# @main.route('/<username>/books/')
# See missing dewey numbers, not to use during production
@main.route('/books_uploaded')
def viewBooks():


    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    books_list = [book.serialize() for book in books]
    return jsonify(books_list)

@main.route('/ten_categories')
def viewCategories():

    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    books_within_categories = [category.to_json() for category in Ten_Categories.query.all()]
    return jsonify(books_within_categories)





# -----------------------------------------------------------------------------------------------
# One time upload of categories, Admin only
# 2 more upload functions

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
          
        return redirect(url_for(".viewCategories", username='john'), code=302)

    return """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """


@main.route('/category/hundred/upload', methods=['GET', 'POST'])
def csv_import_hundred_categories():
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
            table=Hundred_Categories,
            initializer=category_init_func,
            mapdict=mapdict
        )      
          
        return redirect(url_for(".viewCategories", username='john'), code=302)

    return """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """

