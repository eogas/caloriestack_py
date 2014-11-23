import binascii, os
from datetime import date, datetime, timedelta

from caloriestack import db, models

class Stack(db.Model):
	__tablename__ = 'stack'
	id = db.Column(db.String(6), primary_key=True)
	lastReminder = db.Column(db.DateTime())
	bookmarked = db.Column(db.Boolean()) # todo

	def __init__(self, id=None):
		self.id = id

		if self.id is None:
			self.id = Stack.__generateStackId()

	def needsReminder(self):
		# don't show reminders for the sample stack
		if self.id == "sample":
			return False

		# new stack, no reminders seen yet
		if self.lastReminder is None:
			return True

		# todo, make this delta configurable
		return self.lastReminder < (datetime.now() - timedelta(days=1))

	def __repr__(self):
		return '<Stack %r>' % self.id

	def __generateStackId():
		return binascii.hexlify(os.urandom(3)).decode('utf-8')
