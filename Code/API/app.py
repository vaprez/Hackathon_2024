from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://car_fleet_user:edfCorsica@localhost:5432/car_fleet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define a simple model to test
class Voiture(db.Model):
    __tablename__ = 'voitures'
    immat = db.Column(db.String(20), primary_key=True)
    propulsion = db.Column(db.String(50), nullable=False)
    nb_places = db.Column(db.Integer, nullable=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
