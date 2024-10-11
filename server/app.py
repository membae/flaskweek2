#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route("/restaurants")
def get():
    restaurants=Restaurant.query.all()
    restaurants_data=[restaurant.to_dict(only=('id','name','address'))for restaurant in restaurants]
    return make_response(restaurants_data),200

@app.route("/restaurants/<int:id>")
def get_by_id(id):
    restaurant=Restaurant.query.filter_by(id=id).first()
    if restaurant:
        return make_response(restaurant.to_dict(),200)
    return make_response({'error':'Restaurant not found'},404)

@app.route("/restaurants/<int:id>",methods=['DELETE'])
def delete(id):
    restaurant=Restaurant.query.filter_by(id=id).first()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response("",204)
    return make_response({"error":"Restaurant not found"},404)

@app.route("/pizzas")
def get_pizzas():
    pizzas=Pizza.query.all()
    pizzas_data=[pizza.to_dict(only=("id",'name','ingredients'))for pizza in pizzas]
    return make_response(pizzas_data),200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
