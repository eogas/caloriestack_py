import json

from caloriestack import app, db
from caloriestack.models.FoodItem import FoodItem
from caloriestack.models.Meal import Meal
from flask import request

@app.route('/fooditem', methods=['GET'])
def fooditem_list():
	return json.dumps(list(item.json() for item in FoodItem.query.all()))

@app.route('/fooditem/<int:id>', methods=['GET'])
def fooditem_get(id):
	return json.dumps(FoodItem.query.get(id).json())

@app.route('/fooditem', methods=['POST'])
def fooditem_add():
	data = request.get_json()

	name = data['name']
	cals = int(data['cals'])
	mealId = int(data['mealId'])

	item = FoodItem(name=name, cals=cals)
	item.meal = Meal.query.get(mealId)

	db.session.add(item)
	db.session.commit()

	return json.dumps(item.json())

@app.route('/fooditem/<int:id>', methods=['PUT'])
def fooditem_edit(id):
	data = request.get_json()
	item = FoodItem.query.get(id)
	if data['name']: item.name = data['name']
	if data['cals']: item.cals = int(data['cals'])

	db.session.commit()

	return json.dumps(item.json())

@app.route('/fooditem/<int:id>', methods=['DELETE'])
def fooditem_delete(id):
	item = FoodItem.query.get(id)
	itemJson = item.json()

	db.session.delete(item);
	db.session.commit();

	return json.dumps(itemJson)
