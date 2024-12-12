# app.py
from flask import Flask, jsonify, request
from models import db, Voiture
from services import get_voitures, get_voiture, get_kilometrage, post_kilometrage

app = Flask(__name__)
app.json.sort_keys = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://car_fleet_user:edfCorsica@localhost:5432/car_fleet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/voitures', methods=['GET'])
def voitures():
    return jsonify(get_voitures())

@app.route('/voiture/<immat>', methods=['GET'])
def voiture(immat):
    voiture = get_voiture(immat)
    if voiture:
        return jsonify(voiture)
    else:
        abort(404, description="Voiture non trouvée")

@app.route('/voiture/<immat>/kilometrage', methods=['GET'])
def kilometrage(immat):
    return jsonify(get_kilometrage(immat))

@app.route('/voiture/<immat>/kilometrage', methods=['POST'])
def add_kilometrage(immat):

    data = request.get_json()

    # Vérifier que les champs obligatoires sont présents
    if not data or 'releve_km' not in data or 'source_releve' not in data:
        return jsonify({'error': 'Les champs "releve_km" et "source_releve" sont obligatoires.'}), 400

    releve_km = data['releve_km']
    source_releve = data['source_releve']

    # Appeler la fonction du service pour créer le relevé
    result, status_code = post_kilometrage(immat, releve_km, source_releve)


    return jsonify(result), status_code


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)
