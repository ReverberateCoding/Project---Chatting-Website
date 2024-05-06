from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'

class LoginForm(FlaskForm):
  username = StringField('Email Address', validators=[Email(message='Invalid email address')])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=15)])

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def index():
  form = LoginForm()

  if form.validate_on_submit():
      print("lmao")
      # Process the form data (e.g., authenticate user)
      username = form.username.data
      password = form.password.data
      print(username)
      print(password)
      # Add your authentication logic here

      # For example, after authentication:
      return redirect(url_for('home'))

  return render_template('index.html', form=form)

if __name__ == "__main__":
  print("Running app")
  app.run(debug=True)
