import os

# Get auto assigned port, or fall back to 5000
port = os.environ.get('PORT')
if port is None:
	port = 5000

from caloriestack import app

if __name__ == '__main__':
	app.run(debug=True, port=port)
