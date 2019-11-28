from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)  # first check this statement in any file and at the file location search for template folder
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# myapp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost:3306/pydb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# myapp.config['SECRET_KEY'] = 'abcdefoasjksadkop'  # this is for client -server communication security
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(64),
                         index=False,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    hash_password = db.Column(db.String(240),
                              nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
