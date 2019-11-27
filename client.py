import os
import zmq
from functools import wraps
from flask import flash, session, redirect, url_for, request, render_template, json
from passlib.hash import sha256_crypt
from models import app, db, User

context = zmq.Context()
socket = context.socket(zmq.SUB)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap


def enc_password(password):
    result = sha256_crypt.encrypt(password)
    return result


def verify_password(password1, password2):
    return sha256_crypt.verify(password1, password2)


@app.route('/')
@login_required
def home():
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(os.environ['server_url'])
    return render_template('home.html', server_url=os.environ['server_url'])


@app.route("/login", methods=['POST', 'GET'])
def user_login():
    # req_dict = req.get_json()
    if request.method == "POST":
        req_dict = request.form
        user = User.query.filter_by(username=req_dict.get('username')).first()
        if user and verify_password(req_dict.get('password'), user.hash_password):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return render_template('home.html', context=user.username)
        return "Check username/password!"

    else:
        return render_template('login.html')


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('index'))


@app.route("/register", methods=['POST', 'GET'])
def create_user():
    # request_dict = request.get_json()
    if request.method == "POST":
        request_dict = request.form
        user = User(username=request_dict.get('username'), email=request_dict.get('email'),
                    hash_password=enc_password(request_dict.get('password')))
        db.session.add(user)
        db.session.commit()
        db.session.remove()
        return render_template('login.html')
    else:
        return render_template('register.html')


@app.route('/message')
def message():
    message = socket.recv()

    response = app.response_class(
        response=json.dumps({'message': message.decode("utf-8")}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=False)
