import binascii, os
from datetime import date, datetime, timedelta

from caloriestack import db, models

#
# TODO: Remember to fix the lack of a composite key here when switching away from sqlite
#

class StackDay(db.Model):
	__tablename__ = 'stackday'
	id = db.Column(db.Integer(), autoincrement=True, primary_key="True")
	day = db.Column(db.Date())

	stackId = db.Column('stackId', db.String(6), db.ForeignKey('stack.id'))
	stack = db.relationship('Stack', backref=db.backref('days', lazy='dynamic'))

	def __init__(self, day=None):
		self.day = day

		if self.day is None:
			self.day = date.today()

	def cals(self):
		total = 0

		for meal in self.meals:
			total += meal.cals()

		return total

	def json(self):
		jsonObj = {}
		jsonObj['stackId'] = self.stack.id
		#jsonObj['day'] = self.day
		jsonObj['cals'] = self.cals()
		jsonObj['meals'] = list(meal.json() for meal in self.meals)
		jsonObj['reminder'] = self.stack.needsReminder()

		return jsonObj

	def __repr__(self):
		return '<StackDay %r:%r>' % (self.id, self.day)

	def __generateStackId():
		return binascii.hexlify(os.urandom(3)).decode('utf-8')
