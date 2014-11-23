from datetime import date

from caloriestack import app
from flask import render_template

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<string:id>')
def stack(id):
	day = date.today()
	return render_template('stack.html',
		stackId=id,
		year=day.year,
		month=day.month,
		day=day.day)

@app.route('/<string:id>/<int:year>/<int:month>/<int:day>')
def stackWithDay(id, year, month, day):
	return render_template('stack.html',
		stackId=id,
		year=year,
		month=month,
		day=day)
