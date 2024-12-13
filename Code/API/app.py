from flask import Flask, jsonify, request, abort
from models import db
from services import get_voitures, get_voiture, get_kilometrage, post_kilometrage, dernier_kilometrage, get_defauts_veh, post_defaut_veh    
from detect import *

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


# liste retourne dernier kilometre, trie par plus grand
@app.route('/voiture/<immat>/dernier_kilometrage', methods=['GET'])
def kilometre_last(immat):
    return jsonify(dernier_kilometrage(immat))


# Ajouter des defauts a un véhicule
@app.route('/voiture/add_defauts', methods=['POST'])
def add_defaut_veh():
    data = request.get_json()
    # print(data)
    # defauts_veh_list = []
    for defaut_veh in data:
        # print(defaut_veh)
        # Vérifier que les champs obligatoires sont présents
        if not defaut_veh or 'immat' not in defaut_veh or 'id_defaut' not in defaut_veh or 'commentaire_libre' not in defaut_veh :
            return jsonify({'error': 'Les champs "immat", "commentaire_libre" et "id_defaut" sont obligatoires.'}), 400
        
        immat = defaut_veh['immat']
        id_defaut = defaut_veh['id_defaut']
        commentaire_libre = defaut_veh['commentaire_libre']

        result, status_code = post_defaut_veh(immat, id_defaut, commentaire_libre)
 
    return jsonify(result),status_code


# Afficher les defauts d'un véhicule
@app.route('/voiture/<immat>/defauts', methods=['GET'])
def defauts_veh(immat):
   return jsonify(get_defauts_veh(immat))


@app.route('/vehicule/immat_ocr', methods=['POST'])
def vehicule_imat():
    data = request.get_json()
    if not data or 'blob' not in data:
        return jsonify({'error': 'Aucune chaîne de texte trouvée dans le JSON'}), 400
    blob = data['blob']
    image_bytes,extension = base64_to_image(blob)
    image = create_image_from_bytes(image_bytes)
    image_path = save_image(image,extension)
    detected_plate = immat_recognition(image_path)
    return jsonify(detected_plate)


@app.route('/vehicule/compteur',methods=['POST'])
def vehicule_km():
    data = request.get_json()
    if not data or 'blob' not in data:
            return jsonify({'error': 'Aucune chaîne de texte trouvée dans le JSON'}), 400
    blob = data['blob']
    image_bytes,extension = base64_to_image(blob)
    image = create_image_from_bytes(image_bytes)
    image_path = save_image(image,extension)
    detected_km = kilommetrage_recognition(image_path)
    return jsonify(detected_km)






if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)

