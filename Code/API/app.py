# app.py
from flask import Flask, jsonify, request
from models import db, Voiture
from services import  get_voitures, get_voiture,get_defauts_veh,post_defaut_veh

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
def vehicules():
    return jsonify(get_voitures())

@app.route('/voiture/<immat>', methods=['GET'])
def vehicule(immat):
    return jsonify(get_voiture(immat))

# Ajouter des defauts a un véhicule
@app.route('/voiture/add_defauts', methods=['POST'])
def add_defaut_veh():
    data = request.get_json()
    
    defauts_veh_list = []
    for defaut_veh in data:
        
         # Vérifier que les champs obligatoires sont présents
        if not defaut_veh or 'immat' not in defaut_veh or 'id_defaut' not in defaut_veh or 'commentaire_libre' not in defaut_veh :
            return jsonify({'error': 'Les champs "immat", "commentaire_libre" et "id_defaut" sont obligatoires.'}), 400

        immat = defaut_veh['immat']
        id_defaut = defaut_veh['id_defaut']
        commentaire_libre = defaut_veh['commentaire_libre']

        result, status_code = defauts_veh_list.append(post_defaut_veh(immat, id_defaut, commentaire_libre))
    return jsonify(result), status_code





# Afficher les defauts d'un véhicule
@app.route('/voiture/<immat>/defauts', methods=['GET'])
def defauts_veh(immat):
   return jsonify(get_defauts_veh(immat))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)
