import logging
import json
import os
import uuid

from flask_cors import CORS
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:1234@/schema'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    user_id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(50), nullable=False)

    def __init__(self, first_name, last_name, user_password, email, phone_number, address):
        self.user_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.user_password = user_password
        self.email = email
        self.phone_number = phone_number
        self.address = address


class Sessions(db.Model):
    session_id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    expiry_date = db.Column(db.DATETIME, db.ForeignKey('users.user_id'))

    def __init__(self, user_id, expiry_date):
        self.session_id = str(uuid.uuid4())
        self.user_id = user_id
        self.expiry_date = str(expiry_date)


@app.route('/session', methods=['GET'])
def get_session():

    print("GET SESSION\n====================================================")

    session_id = request.args.get("session_id")

    session = Sessions.query.filter_by(session_id=session_id).first()

    if session is None:
        response = {
            "session_id": None,
            "user_id": None,
            "expiry_date": None
        }

        print(response)

        return json.dumps(response), 404, {'Content-Type': 'application/json'}
    else:
        response = {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "expiry_date": str(session.expiry_date)
        }

        print(response)

        return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/session', methods=['POST'])
def insert_session():

    print("POST SESSION\n====================================================")

    content = json.loads(json.loads(request.data)["body"])

    user_id = content["user_id"]
    expiry_date = content["expiry_date"]

    session = Sessions(
        user_id=user_id,
        expiry_date=expiry_date
    )

    db.session.add(session)
    db.session.commit()

    response = {
        "session_id": session.session_id,
        "user_id": session.user_id,
        "expiry_date": str(session.expiry_date)
    }

    return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/user', methods=['GET'])
def get_user():

    print("LOGIN\n====================================================")
    email = request.args.get('email')
    user_password = request.args.get('user_password')

    user = Users.query.filter_by(email=email, user_password=user_password).first()

    if user is None:
        response = {
            "user_id": None,
            "first_name": None,
            "last_name": None,
            "user_password": None,
            "email": None,
            "phone_number": None,
            "address": None
        }
        print(response)

        return json.dumps(response), 404, {'Content-Type': 'application/json'}

    else:
        response = {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_password": user.user_password,
            "email": user.email,
            "phone_number": user.phone_number,
            "address": user.address
        }

        print(response)

        return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/user', methods=['POST'])
def insert_user():

    print("REGISTER\n====================================================")

    # print(str(json.loads(json.loads(request.data))))
    content = json.loads(json.loads(request.data)["body"])
    print("JSON: " + str(content))

    first_name = content["first_name"]
    last_name = content["last_name"]
    user_password = content["user_password"]
    email = content["email"]
    phone_number = content["phone_number"]
    address = content["address"]

    user = Users(
        first_name=first_name,
        last_name=last_name,
        user_password=user_password,
        email=email,
        phone_number=phone_number,
        address=address
    )

    db.session.add(user)
    db.session.commit()

    response = {
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_password": user.user_password,
        "email": user.email,
        "phone_number": user.phone_number,
        "address": user.address
    }

    print(response)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/', methods=['GET'])
def home():

    return json.dumps({}), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
