from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Test route
@app.route('/')
def index():
    return "Bookish backend is running!"

if __name__ == '__main__':
    app.run(debug=True)