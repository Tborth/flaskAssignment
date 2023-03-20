from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import  LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,static_folder="static")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'login.db'


db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'key-----'
login_manager = LoginManager()
login_manager.init_app(app)
from route import *
# app.register_blueprint(form_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

