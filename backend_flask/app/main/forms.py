from flask_wtf import FlaskForm
from wtforms import FileField , SubmitField

class UploadFile(FlaskForm):
    csv_file = FileField('CSV File'])
    submit = SubmitField('Upload File')