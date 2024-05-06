from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'

class LoginForm(Form):
  username = StringField('Username', validators=[validators.InputRequired()])
  password = PasswordField('Password', validators=[validators.InputRequired()])


@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/', methods=['GET','POST'])
def index():
  temp_form = LoginForm()
  return render_template('index.html', form=temp_form)

if __name__ == "__main__":
  app.run(debug=True)