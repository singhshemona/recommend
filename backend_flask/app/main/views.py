from flask import render_template, jsonify, request
from . import main
import flask_excel as excel

@main.route('/')
def index():
    # return '<h1>Home Page</h1>'
    return render_template('index.html')



# jsonify + request imports
@main.route('/bookshelf', methods=['GET', 'POST'])
def bookshelf_user():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''

    # return render_template('bookshelf.html')



