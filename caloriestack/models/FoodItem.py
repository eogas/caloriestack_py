
from caloriestack import db, models

class FoodItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	cals = db.Column(db.Integer)

	mealId = db.Column(db.Integer, db.ForeignKey('meal.id'))
	meal = db.relationship('Meal', backref=db.backref('items', lazy='dynamic'))

	def json(self):
		jsonObj = {}
		jsonObj['id'] = self.id
		jsonObj['name'] = self.name
		jsonObj['cals'] = self.cals
		jsonObj['mealId'] = self.mealId

		return jsonObj

	def __repr__(self):
		return '<FoodItem %r:%r:%r>' % (self.mealId, self.name, self.cals)
