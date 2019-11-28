import os
import zmq
from flask import Flask, render_template, json, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from models import app, db, User

context = zmq.Context()
socket = context.socket(zmq.SUB)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def authenticate(username, password):
    req_dict = request.get_json()
    user = User.query.filter_by(username=req_dict.get('username')).first()
    password = req_dict.get('password')
    if user and safe_str_cmp(user.hash_password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return 1


jwt = JWT(app, authenticate, identity)


@app.route('/')
@jwt_required()
def home():
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect("tcp://0.0.0.0:5555")
    return render_template('home.html', server_url="tcp://0.0.0.0:5555")


@app.route("/login", methods=['POST', 'GET'])
def user_login():
    if request.method == "POST":
        req_dict = request.get_json()
        # req_dict = request.form
        user = User.query.filter_by(username=req_dict.get('username')).first()
        if user:
            return render_template('home.html', context=user.username)
        return "Check username/password!"

    else:
        return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def create_user():
    print(request)
    if request.method == "POST":
        request_dict = request.get_json()
        # request_dict = request.form
        print(request_dict.get('username'))
        user = User(username=request_dict.get('username'), email=request_dict.get('email'),
                    hash_password=request_dict.get('password'))
        db.session.add(user)
        db.session.commit()
        db.session.remove()
        #return render_template('login.html')
        return "User created successfully!"
    else:
        #return render_template('register.html')
        pass


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
    db.create_all()
    app.run(debug=True, port=5001)
