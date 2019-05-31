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


class Items(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    restaurant_id = db.Column(db.String(36), nullable=False)

    def __init__(self, name, restaurant_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.restaurant_id = restaurant_id


class Restaurants(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    restaurant_name = db.Column(db.String(30), nullable=False)
    restaurant_image = db.Column(db.String(200), nullable=False)

    def __init__(self, restaurant_name, restaurant_image):
        self.restaurant_name = restaurant_name
        self.restaurant_image = restaurant_image


class Couriers(db.Model):
    courier_id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    courier_password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    busy = db.Column(db.Boolean, nullable=False)

    def __init__(self, first_name, last_name, courier_password, email, phone_number):
        self.courier_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.courier_password = courier_password
        self.email = email
        self.phone_number = phone_number
        self.busy = False


class Orders(db.Model):
    order_id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    courier_id = db.Column(db.String(36), nullable=False)
    items = db.Column(db.String, nullable=False)
    client_address = db.Column(db.String(36), nullable=False)
    client_first_name = db.Column(db.String(36), nullable=False)
    client_last_name = db.Column(db.String(36), nullable=False)
    client_phone_number = db.Column(db.String(36), nullable=False)
    restaurant_address = db.Column(db.String(200), nullable=False)
    restaurant_name = db.Column(db.String(50), nullable=False)

    def __init__(self, courier_id, items, client_address, client_first_name, client_last_name, client_phone_number, restaurant_name, restaurant_address):
        self.order_id = str(uuid.uuid4())
        self.courier_id = courier_id
        self.items = items
        self.client_address = client_address
        self.client_first_name = client_first_name
        self.client_last_name = client_last_name
        self.client_phone_number = client_phone_number
        self.restaurant_address = restaurant_address
        self.restaurant_name = restaurant_name


class Sessions(db.Model):
    session_id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    expiry_date = db.Column(db.DATETIME, db.ForeignKey('users.user_id'))

    def __init__(self, user_id, expiry_date):
        self.session_id = str(uuid.uuid4())
        self.user_id = user_id
        self.expiry_date = str(expiry_date)


class SessionsCouriers(db.Model):
    session_id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    courier_id = db.Column(db.String(36), nullable=False)
    expiry_date = db.Column(db.DATETIME, db.ForeignKey('couriers.courier_id'))

    def __init__(self, courier_id, expiry_date):
        self.session_id = str(uuid.uuid4())
        self.courier_id = courier_id
        self.expiry_date = str(expiry_date)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurants.query.all()
    response = {"restaurants": []}

    for restaurant in restaurants:
        database_restaurant = {
            "id": restaurant.id,
            "restaurant_name": restaurant.restaurant_name,
            "restaurant_image": restaurant.restaurant_image
        }
        response["restaurants"].append(database_restaurant)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}


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


@app.route('/session', methods=['GET'])
def get_session_courier():

    print("GET SESSION\n====================================================")

    session_id = request.args.get("session_id")

    session = SessionsCouriers.query.filter_by(session_id=session_id).first()

    if session is None:
        response = {
            "session_id": None,
            "courier_id": None,
            "expiry_date": None
        }

        print(response)

        return json.dumps(response), 404, {'Content-Type': 'application/json'}
    else:
        response = {
            "session_id": session.session_id,
            "courier_id": session.courier_id,
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


@app.route('/courier/session', methods=['POST'])
def insert_session_courier():

    print("POST SESSION\n====================================================")

    content = json.loads(json.loads(request.data)["body"])

    print(content)

    courier_id = content["courier_id"]
    expiry_date = content["expiry_date"]

    session = SessionsCouriers(
        courier_id=courier_id,
        expiry_date=expiry_date
    )

    db.session.add(session)
    db.session.commit()

    response = {
        "session_id": session.session_id,
        "courier_id": session.courier_id,
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


@app.route('/courier', methods=['GET'])
def get_courier():

    print("LOGIN\n====================================================")
    email = request.args.get('email')
    courier_password = request.args.get('courier_password')

    courier = Couriers.query.filter_by(email=email, courier_password=courier_password).first()

    if courier is None:
        response = {
            "courier_id": None,
            "first_name": None,
            "last_name": None,
            "courier_password": None,
            "email": None,
            "phone_number": None,
            "busy": None
        }
        print(response)

        return json.dumps(response), 404, {'Content-Type': 'application/json'}

    else:
        response = {
            "courier_id": courier.courier_id,
            "first_name": courier.first_name,
            "last_name": courier.last_name,
            "courier_password": courier.courier_password,
            "email": courier.email,
            "phone_number": courier.phone_number,
            "busy": False
        }

        print(response)

        return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/user/session', methods=['GET'])
def get_user_session():
    print("GET SESSION\n====================================================")
    session_id = request.args.get('session_id')

    session = Sessions.query.filter_by(session_id=session_id).first()
    user = Users.query.filter_by(user_id=session.user_id).first()

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


@app.route('/items', methods=['GET'])
def get_items():
    print("GET ITEMS\n====================================================")
    restaurant_name = request.args.get('restaurant_name')

    restaurant = Restaurants.query.filter_by(restaurant_name=restaurant_name).first()
    items = Items.query.filter_by(restaurant_id=restaurant.id).all()

    response = {"items": []}

    for item in items:
        food_item = {
            "id": item.id,
            "name": item.name,
            "restaurant_id": item.restaurant_id
        }
        response["items"].append(food_item)

    print(response)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/courier/session', methods=['GET'])
def get_courier_session():
    print("GET SESSION\n====================================================")
    session_id = request.args.get('session_id')

    session = SessionsCouriers.query.filter_by(session_id=session_id).first()
    courier = Couriers.query.filter_by(courier_id=session.courier_id).first()

    response = {
        "courier_id": courier.courier_id,
        "first_name": courier.first_name,
        "last_name": courier.last_name,
        "courier_password": courier.courier_password,
        "email": courier.email,
        "phone_number": courier.phone_number,
        "busy": courier.busy
    }
    print(response)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/orders', methods=['POST'])
def post_order():

    orders = json.loads(json.loads(request.data.decode())["body"])
    # print(orders)
    user = get_user_session_function(orders[len(orders) - 3])
    order_ids = ""
    for order in orders[:-4]:
        order_ids += order + ","
    order_ids += orders[-4]
    # print(order_ids)
    restaurant_address = orders[-1]
    restaurant_name = orders[-2]

    courier = get_first_courier_available()
    Couriers.query.filter_by(courier_id=courier).first().busy = True
    db.session.commit()

    new_order = Orders(
        client_address=user["address"],
        client_first_name=user["first_name"],
        client_last_name=user["last_name"],
        client_phone_number=user["phone_number"],
        items=order_ids,
        courier_id=courier,
        restaurant_name=restaurant_name,
        restaurant_address=restaurant_address
    )
    db.session.add(new_order)
    db.session.commit()

    return json.dumps({}), 200, {'Content-Type': 'application/json'}


@app.route('/complete', methods=['GET'])
def complete_order_courier():
    order_id = request.args.get('order_id')
    order = Orders.query.filter_by(order_id=order_id).first()
    courier = Couriers.query.filter_by(courier_id=order.courier_id).first()
    courier.busy = False
    order = Orders.query.filter_by(order_id=order_id).delete()
    db.session.commit()
    # db.session.expunge(order)
    db.session.commit()

    return json.dumps({}), 200, {'Content-Type': 'application/json'}  


@app.route('/orders', methods=['GET'])
def get_order_courier():
    session_id = request.args.get('session_id')
    courier_id = SessionsCouriers.query.filter_by(session_id=session_id).first().courier_id

    order = Orders.query.filter_by(courier_id=courier_id).first()

    if order is None:
        return json.dumps({}), 200, {'Content-Type': 'application/json'}
    else:
        response = {
            "order_id": order.order_id,
            "client_first_name": order.client_first_name,
            "client_last_name": order.client_last_name,
            "client_address": order.client_address,
            "client_phone_number": order.client_phone_number,
            "restaurant_name": order.restaurant_name,
            "restaurant_address": order.restaurant_address,
            "items": []
        }
        items = order.items.split(",")
        for item in items:
            response["items"].append(get_name(item))

        return json.dumps(response), 200, {'Content-Type': 'application/json'}


def get_name(id):
    item = Items.query.filter_by(id=id).first()
    return item.name


def get_user_session_function(session_id):

    session = Sessions.query.filter_by(session_id=session_id).first()
    user = Users.query.filter_by(user_id=session.user_id).first()

    response = {
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_password": user.user_password,
        "email": user.email,
        "phone_number": user.phone_number,
        "address": user.address
    }

    return response


def get_first_courier_available():
    courier = Couriers.query.filter_by(busy=False).first()
    return courier.courier_id


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


@app.route('/courier', methods=['POST'])
def insert_courier():

    print("REGISTER\n====================================================")

    # print(str(json.loads(json.loads(request.data))))
    content = json.loads(json.loads(request.data)["body"])
    print("JSON: " + str(content))

    first_name = content["first_name"]
    last_name = content["last_name"]
    courier_password = content["courier_password"]
    email = content["email"]
    phone_number = content["phone_number"]
    busy = content["busy"]

    courier = Couriers(
        first_name=first_name,
        last_name=last_name,
        courier_password=courier_password,
        email=email,
        phone_number=phone_number,
    )

    db.session.add(courier)
    db.session.commit()

    response = {
        "user_id": courier.courier_id,
        "first_name": courier.first_name,
        "last_name": courier.last_name,
        "courier_password": courier.courier_password,
        "email": courier.email,
        "phone_number": courier.phone_number,
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
    for i in range(1, 40):
        print(uuid.uuid4())
    return json.dumps({}), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
