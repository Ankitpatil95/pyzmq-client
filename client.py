import os
import zmq

from flask import Flask, flash
from flask import Flask, render_template, json


app = Flask(__name__)
context = zmq.Context()
socket = context.socket(zmq.SUB)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home(): 
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(os.environ['server_url'])
    return render_template('home.html', server_url=os.environ['server_url'])


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