from flask import render_template, jsonify, request, url_for, redirect
from . import main
from .. import db
from app.models import Book, User, Ten_Categories, Hundred_Categories, Thousand_Categories
from ..api.books import deweyDecimalLink, deweyToCategoryTen, deweyToCategoryHundred, deweyToCategoryThousand


# from app.models_populate import create_ten_classes, populate_ten_classes, populate_hundred_classes




@main.route('/')
def index():
    return render_template('index.html')

# @main.route('/<username>/books/')
# See missing dewey numbers, not to use during production
@main.route('/circlepacking')
def circlePacking():

    user = User.query.filter_by(username='john').first()
    # books = user.books.all()

    ten_cat = Ten_Categories.query.all()
    ten_cat_list = [ten_category.classification for ten_category in ten_cat]

    hun_cat = Hundred_Categories.query.all()
    hun_cat_list = [hun_category.classification for hun_category in hun_cat]

    thou_cat = Thousand_Categories.query.all()
    thou_cat_list = [thou_category.classification for thou_category in thou_cat]

    tens_list = []
    hun_list = []
    books_dict = {"name" : "books", "children" : tens_list}
    for i in range(len(ten_cat)):
        ten_placeholder = {}
        ten_title = ten_cat[i].classification # string tens list
        ten_placeholder["name"] = ten_title
        ten_placeholder["children"] = hun_list

        for j in ten_cat[i].hundred_values:
            hun_placeholder = {}
            hun_title = j.classification
            hun_placeholder["name"] = hun_title
            hun_placeholder["children"] = []
            hun_list.append(hun_placeholder)


        tens_list.append(ten_placeholder)

    return jsonify(books_dict)


        # hundreds_list = []
        # hundreds_dict = {}
        # for j in ten_cat[i].hundred_values:
        #     hundreds_list.append(j.classification)
        #     for 
        # hundred_title = ten_cat[i].hundred_values # list of 10 hundred val items into ten list
        # books_dict[ten_title] = hundreds_list 
        # # for j in range(len(hun_cat)):
        # #     hun_thous_title = hun_cat[j]
        # #     thousand_title = hun_cat[j].thousand_values

    bookshelf_circle = [
        {
        "name" : "books",
        "children" : [
            {
                "name" : ten_cat[0].classification,
                # "name" : ten_cat[0].call_number + ' | ' + ten_cat[0].classification,
                "children" : [
                    {
                        "name" : ten_cat[0].hundred_values[0].thousand_values[0].classification,
                        "children" : [
                            {
                                    "books" : [ten_cat[0].hundred_values[0].thousand_values[0].books]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ]
    
    return jsonify(bookshelf_circle)


@main.route('/books_uploaded')
def viewBooks():

    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    books_list = [book.serialize() for book in books]
    return jsonify(books_list)

@main.route('/ten_categories')
def viewTenCategories():

    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    books_within_categories = [category.to_json() for category in Ten_Categories.query.all()]
    return jsonify(books_within_categories)


@main.route('/hundred_categories')
def viewHundredCategories():

    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    books_within_categories = [category.to_json() for category in Hundred_Categories.query.all()]
    return jsonify(books_within_categories)


@main.route('/thousand_categories')
def viewThousandCategories():

    user = User.query.filter_by(username='john').first()
    books = user.books.all()

    books_within_categories = [category.to_json() for category in Thousand_Categories.query.all()]
    return jsonify(books_within_categories)




# -----------------------------------------------------------------------------------------------
# One time upload of categories, Admin only

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
          
        return redirect(url_for(".viewTenCategories", username='john'), code=302)

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
            category_instance = Hundred_Categories()
            category_instance.call_number = row['call_number']
            category_instance.classification = row['classification']

            # category_instance = Hundred_Categories_DDC(row['call_number'], row['classification'])
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
          
        return redirect(url_for(".viewHundredCategories", username='john'), code=302)

    return """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """


@main.route('/category/thousand/upload', methods=['GET', 'POST'])
def csv_import_thousand_categories():
    if request.method == 'POST':

        def category_init_func(row):
            category_instance = Thousand_Categories()
            category_instance.call_number = row['call_number']
            category_instance.classification = row['classification']

            # category_instance = Thousand_Categories_DDC(row['call_number'], row['classification'])
            return category_instance

                     
        mapdict = {
            'Call Number' : 'call_number',
            'Classification' : 'classification',
            }

        request.isave_to_database(
            field_name="file",
            session=db.session,
            table=Thousand_Categories,
            initializer=category_init_func,
            mapdict=mapdict
        )      
          
        return redirect(url_for(".viewThousandCategories", username='john'), code=302)

    return """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """


