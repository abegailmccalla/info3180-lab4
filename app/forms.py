from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UploadForm(FlaskForm):
     photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only! (JPG, PNG)')])
     submit = SubmitField('Upload')