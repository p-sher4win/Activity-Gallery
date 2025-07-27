from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileAllowed


# Activity Form
class ActivityForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    images = MultipleFileField("Upload Images", validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'),
        DataRequired()
    ])
    submit = SubmitField("Upload")

# User Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    add = SubmitField("Register")

    # Password setup
    password_hash = PasswordField("Password", validators=[
        DataRequired(),
        EqualTo('password_hash_2', message="Password Doesn't Match!")
    ])
    password_hash_2 = PasswordField("Password (Confirm)", validators=[DataRequired()])

# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")