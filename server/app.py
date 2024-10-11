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

@app.route("/restaurant_pizzas",methods=['POST'])
def create_restaurant_pizza():
    data=request.get_json()

    price=data.get('price')
    pizza_id=data.get('pizza_id')
    restaurant_id=data.get('restaurant_id')

    errors=[]
    if price is None or not isinstance(price,(int,float)) or not(1<=price<=30):
        errors.append("price must be a number")
    if pizza_id is None:
        errors.append("pizza id is required")
    if restaurant_id is None:
        errors.append("restaurant id is required")

    
    if errors:
        return make_response({ "errors": ["validation errors"]},400)
    
    try:
        new_restaurant_pizza=RestaurantPizza(price=price,pizza_id=pizza_id,restaurant_id=restaurant_id)
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        restaurant_pizza_data = {
        "id": new_restaurant_pizza.id,
        "price": new_restaurant_pizza.price,
        "pizza_id": new_restaurant_pizza.pizza_id,
        "restaurant_id": new_restaurant_pizza.restaurant_id,
        "pizza": {
            "id": new_restaurant_pizza.pizza.id,
            "name": new_restaurant_pizza.pizza.name,
            "ingredients": new_restaurant_pizza.pizza.ingredients
        },
        "restaurant": {
            "id": new_restaurant_pizza.restaurant.id,
            "name": new_restaurant_pizza.restaurant.name,
            "address": new_restaurant_pizza.restaurant.address
        }
        
    }
        return make_response(restaurant_pizza_data),201
    except Exception as e:
        return make_response({"errors":[str(e)]}),400
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)
