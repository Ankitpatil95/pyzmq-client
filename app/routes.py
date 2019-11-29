import os
import zmq
from flask import render_template,Flask,flash, request, redirect,url_for, json, session,jsonify,abort
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user,logout_user
from app.models import User
import subprocess
import requests
from functools import wraps


context = zmq.Context()
socket = context.socket(zmq.SUB)

API_URL = os.environ['api_url']
SERVER_URL = os.environ["server_url"]





def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

@app.route('/')
def index():
    return render_template('index.html', title='Home')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        
        # res = requests.post('http://10:0:28:221:5000/auth', json={"username":form.username.data,"password":form.password.data})
        res = requests.post('{}/auth'.format(API_URL), json={"username":form.username.data,"password":form.password.data})
        if res.ok:
            socket.setsockopt(zmq.SUBSCRIBE, b"")
            socket.connect(SERVER_URL)
            return render_template('index.html', title='Home', token=res.json().get('access_token'),server_url=SERVER_URL, user=form.username.data)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():        
        res = requests.post('{}/register'.format(API_URL), json={"username":form.username.data,"password":form.password.data,"email":form.email.data})
        if res.ok:
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/message')
# @login_required
def message():
    message = socket.recv()
    print ("yes its executing")
    response = app.response_class(
        response=json.dumps({'message': message.decode("utf-8")}),
        status=200,
        mimetype='application/json'
    )
    return response




