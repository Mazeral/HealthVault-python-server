from flask import Flask
"""The main file"""


app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


@app.route('/')
def root():
    """Root of our app"""
    return "Hello world!"
