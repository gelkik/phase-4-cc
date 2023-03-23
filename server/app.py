#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants',methods = ["GET"])
def restaurants():
    restaurants = Restaurant.query.all()

    if request.method == "GET":
        restaurants_dict = [restaurants.to_dict() for restaurants in restaurants]

        response = make_response(
            restaurants_dict,
            200
        )
        return response
    
@app.route('/restaurants/<int:id>',methods = ["GET","DELETE"])
def restaurants_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id==id).first()

    if not restaurant:
        response_body = {
            "error": "Restaurant not found"
        }
        response = make_response(
            response_body,
            404
        )
        return response

    elif request.method == "GET":
        restaurant_dict = restaurant.to_dict()

        response = make_response(
            restaurant_dict,
            200
        )
        return response

    elif request.method == "DELETE":
        try:
            db.session.delete(restaurant)
            db.session.commit()

            response = make_response(
                {},
                200
            )
            return response
        
        except:
            response_body = {
                "error": "Restaurant not found"
            }

            response = make_response(
                response_body,
                404
            )
            return response
        
@app.route('/restaurant_pizzas',methods = ['POST'])
def restaurant_pizzas():
    # restaurant_pizzas = RestaurantPizza.query.all()

    # if request.method == 'GET':
    #     restaurant_pizzas_dict = [restaurant_pizzas.to_dict() for restaurant_pizzas in restaurant_pizzas]

    #     response = make_response(
    #         restaurant_pizzas_dict,
    #         200
    #     )
    #     return response
    
    # elif request.method == 'POST':
    try:
        new_restaurant = RestaurantPizza(
            price = request.get_json()['price'],
            pizza_id = request.get_json()['pizza_id'],
            restaurant_id = request.get_json()['restaurant_id']
        )
        db.session.add(new_restaurant)
        db.session.commit()

        new_pizza = Pizza.query.filter(Pizza.id == new_restaurant.pizza_id).first()
        new_dict = new_pizza.to_dict()

        response = make_response(
            jsonify(new_dict),
            201
        )

    except ValueError:
        response_body = {
            "errors": ["validation errors"]
        }
        response = make_response(
            response_body,
            400
        )
    return response
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
