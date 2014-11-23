import json

from caloriestack import app, db
from caloriestack.models.Meal import Meal
from caloriestack.models.FoodItem import FoodItem
from flask import render_template

@app.route('/meal/<int:id>', methods=['get'])
def meal_get(id):
	return json.dumps(Meal.query.get(id).json())
