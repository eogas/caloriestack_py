from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os

app = Flask(__name__,
	static_folder='static',
	static_url_path='')

# Get production DB details, or fall back to dev DB
dburl = os.environ.get('DATABASE_URL', 'postgresql://caloriestack:caloriestack@localhost/caloriestack')

app.config['SQLALCHEMY_DATABASE_URI'] = dburl
db = SQLAlchemy(app)

from caloriestack.models import *

db.drop_all()
db.create_all()

sampleStack = Stack.Stack(id='sample')
sampleStackDay = StackDay.StackDay()
sampleStackDay.stack = sampleStack

db.session.add(sampleStack)
db.session.add(sampleStackDay)

# Generate meals
for mealName in ['Breakfast', 'Lunch', 'Dinner']:
	m = Meal.Meal(name=mealName)
	m.stackDay = sampleStackDay
	db.session.add(m)

# TODO: Replace this with a script after switching to a real DB
eggs = FoodItem.FoodItem(name='Eggs', cals=156, meal=Meal.Meal.query.get(1))
bacon = FoodItem.FoodItem(name='Bacon', cals=184, meal=Meal.Meal.query.get(1))
db.session.add(eggs)
db.session.add(bacon)

burger = FoodItem.FoodItem(name='Burger', cals=550, meal=Meal.Meal.query.get(2))
fries = FoodItem.FoodItem(name='Fries', cals=380, meal=Meal.Meal.query.get(2))
db.session.add(burger)
db.session.add(fries)

db.session.commit()

from caloriestack.routes import *
