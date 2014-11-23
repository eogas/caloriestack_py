
from caloriestack import db

class Meal(db.Model):
	__tablename__ = 'meal'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))

	stackDayId = db.Column(db.Integer(), db.ForeignKey('stackday.id'))
	stackDay = db.relationship('StackDay', backref=db.backref('meals', lazy='dynamic'))

	def cals(self):
		total = 0

		for item in self.items:
			total += item.cals

		return total

	def json(self):
		jsonObj = {}
		jsonObj['id'] = self.id
		jsonObj['name'] = self.name
		jsonObj['cals'] = self.cals()
		jsonObj['items'] = list(item.json() for item in self.items)

		return jsonObj

	def __repr__(self):
		return '<Meal %r>' % (self.name)
