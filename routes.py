from flask import render_template, request
from wtform_field import RegistrationForm
from models import User

def register_routes(app, db):
    @app.route('/', methods=['GET','POST'])
    def index():
        reg_form = RegistrationForm()
        if reg_form.validate_on_submit():
            username_data = reg_form.username.data
            password_data = reg_form.password.data
            if User.query.filter_by(username=username_data).first():
                return "Someone else has taken this username!"
            user = User(username=username_data, password=password_data)
            print(user)
            db.session.add(user)
            db.session.commit()
        users = User.query.all()
        return render_template('index.html',form=reg_form, users=users)