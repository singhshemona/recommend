from flask import render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from . import main
import flask_excel as excel

@main.route('/')
def index():
    # return '<h1>Home Page</h1>'
    return render_template('index.html')



# jsonify + request imports
@main.route('/books/upload', methods=['GET', 'POST'])
def csv_import():
    if request.method == 'POST':

        def goodreads_init_func(row):
            user = User.query.filter_by(id=1)
            b = Book(row['title'], 
                row['book_id'], 
                row['author'], 
                row['additional_authors'], 
                row['ISBN'], 
                row['My Rating'], 
                row['Average Rating'], 
                row['Publisher'], 
                row['Number of Pages'], 
                row['Year Published'], 
                row['Original Publication Year'], 
                row['Date Read'], 
                row['Date Added'], 
                row['Bookshelves'],
                user)
            return b

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Book],
            initializers=[goodreads_init_func])
        return redirect(url_for('.handson_table'), code=302)
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''

    # return render_template('bookshelf.html')



