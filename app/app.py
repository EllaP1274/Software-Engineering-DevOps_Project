from flask import Flask
app = Flask(__name__)

# Import routes and other necessary modules
from routes import *

if __name__ == "app":
    app.run(debug=True)
