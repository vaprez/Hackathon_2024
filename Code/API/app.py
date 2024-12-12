# app.py
from flask import Flask, jsonify
from models import db, Vehicule
from services import get_vehicules, get_vehicule

app = Flask(__name__)
app.json.sort_keys = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://car_fleet_user:edfCorsica@localhost:5432/car_fleet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/vehicules', methods=['GET'])
def vehicules():
    return jsonify(get_vehicules())

@app.route('/vehicule/<immat>', methods=['GET'])
def vehicule(immat):
    return jsonify(get_vehicule(immat))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)
