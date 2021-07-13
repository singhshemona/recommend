from flask_wtf import FlaskForm
from wtforms import FileField , SubmitField

class UploadFile(FlaskForm):
    importFile = SubmitField('Import File')
    csv_file = FileField('CSV File')
    upload = SubmitField('Upload') 
    # UploadFile is a subclass of WTForm 
    