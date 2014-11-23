import json
from datetime import date, datetime

from caloriestack import app, db
from caloriestack.models.Meal import Meal
from caloriestack.models.Stack import Stack
from caloriestack.models.StackDay import StackDay
from flask import render_template

@app.route('/stack/<string:id>', methods=['GET'])
def stack_get(id):
	return stack_getWithDay(id, date.today())

@app.route('/stack/<string:id>/<int:year>/<int:month>/<int:day>', methods=['GET'])
def stack_getWithYMD(id, year, month, day):
	stackDay = date(year, month, day)
	return stack_getWithDay(id, stackDay)

def stack_getWithDay(id, day):
	stack = Stack.query.get(id)

	if stack is None:
		stack = Stack()

	stackDay = [sd for sd in stack.days if sd.day == day]

	if len(stackDay) == 0:
		stackDay = StackDay(day=day)
		stackDay.stack = stack
		db.session.add(stackDay)

		for mealName in ['Breakfast', 'Lunch', 'Dinner']:
			meal = Meal(name=mealName)
			meal.stackDay = stackDay
			db.session.add(meal)

		db.session.commit()
	else:
		stackDay = stackDay[0]

	stackJSON = json.dumps(stackDay.json())

	# reset last reminder time
	if stack.needsReminder():
		stack.lastReminder = datetime.now()
		db.session.commit()

	return stackJSON

@app.route('/stack', methods=['POST'])
def stack_add():
	stack = Stack()
	stackDay = StackDay()
	stackDay.stack = stack

	for mealName in ['Breakfast', 'Lunch', 'Dinner']:
		meal = Meal(name=mealName)
		meal.stackDay = stackDay
		db.session.add(meal)

	db.session.add(stack)
	db.session.add(stackDay)
	db.session.commit()

	return json.dumps(stackDay.json())
