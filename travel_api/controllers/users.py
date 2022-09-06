import uuid
from http import HTTPStatus

from db import transactions
from flask import Flask, request
from flask_cors import CORS, cross_origin
from travel_api.config import ApiConfig
from travel_api.util import get_token
from flatten_dict import flatten, unflatten
from flatten_dict.reducers import make_reducer
from flatten_dict.splitters import make_splitter

from travel_api.baggage_generator import process_baggage


api = ApiConfig.i("travel_api")

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.post("/register")
def register():
    body = request.json
    body.update({"uuid": str(uuid.uuid4())})

    with api.db.driver.session() as session:
        user = session.write_transaction(transactions.check_user, body.get("email"))

    if user:
        return "User already exists", 400

    with api.db.driver.session() as session:
        _ = session.write_transaction(transactions.register, body)
    return body


@app.get("/login")
def user():
    body = request.json
    username = body.get("username")
    password = body.get("password")
    print(body)

    if username is None or password is None:
        return "Username or password not provided fmm de fronted", 404

    with api.db.driver.session() as session:
        user = session.read_transaction(transactions.login, username, password)

    if not user:
        return "Login failed", 401

    response = user.data().get("n")
    return response


@app.get("/users")
def users():
    with api.db.driver.session() as session:
        users = session.read_transaction(transactions.get_users)

    response = [record["n"]._properties for record in users]
    return response


@app.get("/users/me")
def users_me():
    token = get_token(request.headers.get("Authorization"))
    if token is not None:
        with api.db.driver.session() as session:
            user = session.read_transaction(transactions.get_user_by_token, token)

        response = user.data().get("n")
        return response
    return "Token not provided", 400


@app.post("/trips")
def create_trip():
    body = request.json
    body.update({"uuid": str(uuid.uuid4()), "bagDone": False})
    visitors = body.pop("visitors")
    weather = body.pop("weather")
    trip = body
    print(trip.get("uuid"))
    with api.db.driver.session() as session:
        _trip = session.write_transaction(
            transactions.create_trip,
            trip,
        )

    with api.db.driver.session() as session:
        _user = session.read_transaction(transactions.get_user, body.get("username"))

    user_data = _user.data().get("n")

    with api.db.driver.session() as session:
        _ = session.write_transaction(
            transactions.add_trip_to_user, trip.get("uuid"), user_data.get("uuid")
        )
    for visitor in visitors:
        visitor.update({"uuid": str(uuid.uuid4()), "bagDone": False})
        with api.db.driver.session() as session:
            _visitor = session.write_transaction(transactions.create_visitor, visitor)
        # visitor_data = _visitor.get("s")._properties
        with api.db.driver.session() as session:
            _ = session.write_transaction(
                transactions.add_visitors_to_trip,
                trip.get("uuid"),
                visitor.get("uuid"),
            )
        baggage = process_baggage(visitor, weather, trip)
        baggage.update({"uuid": visitor.get("uuid")})
        baggage_flatten = flatten(baggage, make_reducer("."))
        with api.db.driver.session() as session:
            _baggage = session.write_transaction(
                transactions.create_baggage, baggage_flatten
            )
        with api.db.driver.session() as session:
            _ = session.write_transaction(
                transactions.add_baggage_to_visitor,
                visitor.get("uuid"),
                baggage.get("uuid"),
            )

    with api.db.driver.session() as session:
        period = {"uuid": trip.get("uuid")}
        _period = session.write_transaction(transactions.create_period, period)

    with api.db.driver.session() as session:
        _ = session.write_transaction(
            transactions.add_period_to_trip, trip.get("uuid"), trip.get("uuid")
        )

    for day in weather:
        day.update({"uuid": str(uuid.uuid4()), "no": weather.index(day)})
        with api.db.driver.session() as session:
            _day = session.write_transaction(transactions.create_day, day)
        day_data = _day.get("s")._properties
        with api.db.driver.session() as session:
            _ = session.write_transaction(
                transactions.add_days_to_period,
                trip.get("uuid"),
                day_data.get("uuid"),
            )
    return body, 200


@app.patch("/trips/<uuid>")
def update_trip():
    body = request.json
    visitors = body.pop("visitors")
    trip = body
    print(trip.get("uuid"))
    with api.db.driver.session() as session:
        _trip = session.write_transaction(
            transactions.create_trip,
            trip,
        )

    with api.db.driver.session() as session:
        _user = session.read_transaction(transactions.get_user, body.get("username"))

    user_data = _user.data().get("n")

    with api.db.driver.session() as session:
        _ = session.write_transaction(
            transactions.add_trip_to_user, trip.get("uuid"), user_data.get("uuid")
        )
    for visitor in visitors:
        visitor.update({"uuid": str(uuid.uuid4())})
        with api.db.driver.session() as session:
            _visitor = session.write_transaction(transactions.create_visitor, visitor)
        with api.db.driver.session() as session:
            _ = session.write_transaction(
                transactions.add_visitors_to_trip,
                trip.get("uuid"),
                visitor.get("uuid"),
            )

    return body, 200


@app.get("/users/<uuid>/trips")
def get_user_trips(uuid):
    with api.db.driver.session() as session:
        user_trips = session.read_transaction(transactions.get_user_trips, uuid)
    trips = []
    response = [record["n"]._properties for record in user_trips]
    for r in response:
        trip = get_trip_info_static(r.get("uuid"))
        trips.append(trip)

    return trips


@app.get("/trips/<uuid>")
def get_trip_info(uuid):
    with api.db.driver.session() as session:
        user_trips = session.read_transaction(transactions.get_trip_visitors, uuid)

    response = [record["n"]._properties for record in user_trips]
    for item in response:
        with api.db.driver.session() as session:
            visitor_baggage = session.read_transaction(
                transactions.get_visitor_baggage, item.get("uuid")
            )
            visitor_baggage = visitor_baggage[0]["t"]._properties
            visitor_baggage = unflatten(visitor_baggage, make_splitter("."))
            item.update({"baggage": visitor_baggage})

    with api.db.driver.session() as session:
        _trip = session.read_transaction(transactions.get_trip_info, uuid)

    trip = _trip.data().get("n")

    with api.db.driver.session() as session:
        _weather = session.read_transaction(transactions.get_trip_weather, uuid)
    weather = [record["d"]._properties for record in _weather]
    final_responde = {"visitors": response, "weather": weather}
    final_responde.update(trip)

    return final_responde


@app.patch("/users")
def patch_user():
    body = request.json

    with api.db.driver.session() as session:
        _ = session.write_transaction(transactions.register, body)
    return body


def get_trip_info_static(uuid):
    with api.db.driver.session() as session:
        user_trips = session.read_transaction(transactions.get_trip_visitors, uuid)

    response = [record["n"]._properties for record in user_trips]
    for item in response:
        with api.db.driver.session() as session:
            visitor_baggage = session.read_transaction(
                transactions.get_visitor_baggage, item.get("uuid")
            )
            visitor_baggage = visitor_baggage[0]["t"]._properties
            visitor_baggage = unflatten(visitor_baggage, make_splitter("."))
            item.update({"baggage": visitor_baggage})

    with api.db.driver.session() as session:
        _trip = session.read_transaction(transactions.get_trip_info, uuid)

    trip = _trip.data().get("n")

    with api.db.driver.session() as session:
        _weather = session.read_transaction(transactions.get_trip_weather, uuid)
    weather = [record["d"]._properties for record in _weather]
    final_responde = {"visitors": response, "weather": weather}
    final_responde.update(trip)

    return final_responde
