from http import HTTPStatus
from flask import Flask, request
from travel_api.config import ApiConfig
from db import transactions
import uuid

api = ApiConfig.i("travel_api")

app = Flask(__name__)


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
    q1 = "MATCH (n) return n"
    with api.db.driver.session() as session:
        nodes = session.run(q1)

    results = [record for record in nodes.data()]
    print(nodes.data())

    return results
