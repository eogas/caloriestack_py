import os

# Get auto assigned port, or fall back to 5000
port = int(os.environ.get('PORT', 5000))

from caloriestack import app

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=port)
