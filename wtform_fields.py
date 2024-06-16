from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from passlib.hash import pbkdf2_sha256
from models import User

def InvalidCredentials(form, field): #WTForm automatically passes in arguements
    username_entered = form.username.data
    password_entered = form.password.data

    user_object = User.query.filter_by(username=username_entered).first()
    #Check if username is valid
    if user_object is None:
        raise ValidationError(message="Username or password is incorrect")
    #Chck if password is valid
    elif not pbkdf2_sha256.verify(password_entered, user_object.hashed_pswd):
        raise ValidationError(message="Username or password is incorrect")


class RegistrationForm(FlaskForm):
    username = StringField('username_label',validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_password = PasswordField('confirm_password_label', validators=[InputRequired(message="Password required"), EqualTo('password', message="Password must match")])
    submit_button = SubmitField("Create")
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError(message="Username already exists. Please select a different username")
        
class LoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), InvalidCredentials])
    submit_button = SubmitField("Login")