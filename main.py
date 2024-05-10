from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtform_field import *
from models import *

app = Flask(__name__)

app.secret_key = 'replace later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/', methods=['GET','POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username_data = reg_form.username.data
        password_data = reg_form.password.data

        user_object = User.query.filter_by(username=username_data).first()
        if user_object:
            return "Someone else has taken this username!"
        else:
            user = User(username=username_data, password=password_data)
            db.session.add(user)
            db.session.commit()
            return "Inserted into DB!"
    return render_template('index.html',form=reg_form)

if __name__ == "__main__":
    app.run(debug=True)