from flask import Flask, jsonify, request, abort
from models import db, Voiture
from services import get_voitures, get_voiture, get_kilometrage, post_kilometrage, dernier_kilometrage, get_defauts_veh, post_defaut_veh, get_destinations, ajout_reservations, reservations_recherche,get_typedefauts
from detect import *

app = Flask(__name__)
app.json.sort_keys = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://car_fleet_user:edfCorsica@localhost:5430/car_fleet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialisation de la base de données
db.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/voitures', methods=['GET'])
def voitures():
    return jsonify(get_voitures())


@app.route('/typedefauts', methods=['GET'])
def typedefauts():
    return jsonify(get_typedefauts())


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

    for defaut_veh in data:
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
    extension = data["extension"]
    image_bytes,extension = base64_to_image(blob,extension)
    image = create_image_from_bytes(image_bytes)
    image_path = save_image(image,extension)
    detected_plate = immat_recognition(image_path)

    if detected_plate:
        return jsonify(detected_plate)
    else:
        return jsonify({'error': 'Aucune plaque détectée'}), 404


@app.route('/vehicule/compteur',methods=['POST'])
def vehicule_km():
    data = request.get_json()
    if not data or 'blob' not in data:
        return jsonify({'error': 'Aucune chaîne de texte trouvée dans le JSON'}), 400

    blob = data['blob']
    extension = data["extension"]
    image_bytes,extension = base64_to_image(blob,extension)
    image = create_image_from_bytes(image_bytes)
    image_path = save_image(image,extension)
    detected_km = kilommetrage_recognition(image_path)
    if (detected_km):
        return jsonify(detected_km)
    else:
        return jsonify({'error': 'Aucun kilométrage détecté'}), 404

@app.route('/destinations', methods=['GET'])
def destinations():
    return jsonify(get_destinations())

@app.route('/reservations', methods=['POST'])
def post_reservations():
    data = request.get_json()
    depart = data.get("depart")
    arrivee = data.get("arrivee")
    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    nb_personnes = data.get("nb_personnes")
    immatriculation = data.get("immat")
    nom_utilisateur = data.get("nom_utilisateur")

    # Validation des données
    if not (depart and arrivee and date_debut and date_fin and nb_personnes and immatriculation and nom_utilisateur):
        return jsonify({"error": "Tous les champs sont requis."}), 400

    Resultats = ajout_reservations(depart,arrivee,date_debut,date_fin,nb_personnes,immatriculation,nom_utilisateur)

    return Resultats


@app.route('/search_reservations',methods=['POST'])
def search_reservations():
    data = request.get_json()
    depart = data.get("depart")
    arrivee = data.get("arrivee")
    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    nb_personnes = data.get("nb_personnes")

    if nb_personnes is None or depart is None or arrivee is None or date_debut is None or date_fin is None:
                return jsonify({"error": "Veuillez fournir 'nb_personnes', 'depart', 'arrivee', 'date_debut' et 'date_fin'."}), 400

    resultats = reservations_recherche(depart,arrivee,date_debut,date_fin,nb_personnes)

    return resultats







if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)

