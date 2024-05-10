from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtform_field import *

app = Flask(__name__)

app.secret_key = 'replace later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)



@app.route('/', methods=['GET','POST'])
def index():
    reg_form = RegistrationForm()
    
    if reg_form.validate_on_submit():
        username_data = reg_form.username.data
        password_data = reg_form.password.data
        print(username_data)
        print(password_data)
    
    return render_template('index.html',form=reg_form)

if __name__ == "_main_":
    app.run(debug=True)