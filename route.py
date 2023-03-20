from flask import Flask, send_file,render_template, request, redirect, url_for,flash
import os

from werkzeug.utils import secure_filename
from flask_login import UserMixin
from sqlalchemy import or_
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import pandas as pd

directory = os.getcwd()

from model import User
from app import app,db

from flask import Blueprint

form_blueprint = Blueprint('form_blueprint', __name__)
#...


@app.before_first_request
def before():
    
    db.create_all()   
  

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Process the file here
        if file.filename.split(".")[-1] == "csv":
            file.save(os.path.join(directory+"/static/upload", secure_filename(file.filename)))
            return render_template('upload_sucessful.html')
        else:
            flash('Upload Csv file ')
            return render_template('failed_upload.html')
    return render_template('upload.html')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_system():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username and password match
        res=db.session.query(User).filter(User.email=='admin').first()
        
        if not res:
            user=User(email= 'admin', password ='admin')
            db.session.add(user)
            db.session.commit()
        for user in User.query.all():
       
            print(user.email)
            print(user.password)
            if (user.email == username and user.password == password) or (username =="admin" and password =="admin"):
                # Redirect to dashboard if login successful
                login_user(user)
                return redirect(url_for('dashboard'))
        # Show error message if login failed
        error = 'Invalid username or password'
        return render_template('signUp.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def signUp():
    if request.method == 'POST':
        username = request.form['username']
        pas = request.form['password']
        print(username)
        print(pas)
        users = User(email= username, password =pas)
        db.session.add(users)
        db.session.commit()
        return render_template('login.html')

    return render_template('signUp.html')

@app.route('/dashboard')
@login_required
def dashboard():
    folder_path = directory+"/static/upload"
    file_names = os.listdir(folder_path)
    print(file_names)
    
    return render_template('dashboard.html', users=file_names)

@app.route('/download/<file_name>')
@login_required
def download(file_name):
 
    file_path = directory+"/static/upload/"+file_name
    # file_names = os.listdir(folder_path)
    return send_file(file_path, as_attachment=True)

    
    return render_template('dashboard.html', users=file_names)

@app.route('/show/<file_name>')
@login_required
def show(file_name):

    file_path = directory+"/static/upload/"+file_name
    # file_names = os.listdir(folder_path)
    data = pd.read_csv(file_path)
    head1=data.head(1)
    print(type(head1))
    # raise ValueError("error")
    return render_template('data.html', filedata=data,filename=file_name)

@app.route('/logout')
@login_required
def logout():
   
    logout_user()
    return redirect(url_for('home'))

