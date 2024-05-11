from flask import render_template, request, redirect, url_for
from wtform_field import RegistrationForm, LoginForm
from models import User

def register_routes(app, db):
    @app.route('/', methods=['GET','POST'])
    def index():
        reg_form = RegistrationForm()
        if reg_form.validate_on_submit():
            username_data = reg_form.username.data
            password_data = reg_form.password.data
            user = User(username=username_data, password=password_data)
            print(user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        users = User.query.all()
        return render_template('index.html',form=reg_form, users=users)
    
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        login_form = LoginForm()
        if login_form.validate_on_submit():
            return "Logged in!"
        return render_template("login.html", form=login_form)