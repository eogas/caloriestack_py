import os

# Get auto assigned port, or fall back to 5000
port = os.environ['PORT']
if port is None:
	port = 5000

from caloriestack import app
app.run(debug=False, port=port)
