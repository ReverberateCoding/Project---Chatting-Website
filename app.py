import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_migrate import Migrate
from gevent import monkey

from wtform_fields import *
from models import *

# Monkey patching is necessary to make standard library 
# cooperative with gevent
monkey.patch_all()

# Configure app
app = Flask(__name__, template_folder='templates')
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb.db'
db.init_app(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app, async_mode='gevent')
ROOMS = ["lounge", "news", "games", "coding"]

# Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Configure migrate
migrate = Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    # Update database if registration is successful
    if reg_form.validate_on_submit():
        # Get username and password
        username_data = reg_form.username.data
        password_data = reg_form.password.data
        # Get hashed password
        hashed_pswd = pbkdf2_sha256.hash(password_data)

        # Add user object to db
        user = User(username=username_data, hashed_pswd=hashed_pswd)
        print(user)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')

        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('index.html', form=reg_form, users=users)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    # Allow login if validation is successful
    if login_form.validate_on_submit():
        # Get user object to pass into flask login
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        # Redirect to chat page
        return redirect(url_for('chat'))
    return render_template("login.html", form=login_form)

@app.route("/logout", methods=['GET'])
def logout():
    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@socketio.on('message')
def message(data):
    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    print(f"\n\n{data}\n\n")
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

@socketio.on('join')
def join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send({'msg': f'{username} has joined the {room} room.'}, room=room)

@socketio.on('leave')
def leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send({'msg': f'{username} has left the {room} room.'}, room=room)

if __name__ == '__main__': 
    socketio.run(app, host='0.0.0.0', port=2002)
