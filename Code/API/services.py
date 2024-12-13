# services.py
from flask import  jsonify
from models import db, Voiture, RelevesKilometres, Defautsremarque
from datetime import date
import googlemaps , json,requests

# Récupérer la clé API depuis les variables d'environnement
GOOGLE_MAPS_API_KEY='AIzaSyBQPPO-ZmcSChn0Q7eRfleBX_aMRM-AUvY'

# Initialiser Flask et le client Google Maps
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

#url de l'API  de calcul d'émission de CO2
urlCO2E = "https://carbonsutra1.p.rapidapi.com/vehicle_estimate_by_type" 


def get_voitures():
    voitures = Voiture.query.all()
    return [voiture.to_dict() for voiture in voitures]

def get_voiture(immat):
    voiture = Voiture.query.get(immat)
    if voiture:
        return voiture.to_dict()

def get_kilometrage(immat):
    releves = RelevesKilometres.query.filter_by(immat=immat).all()
    return [releve.to_dict() for releve in releves]

def post_kilometrage(immat, releve_km, source_releve):
    if not isinstance(releve_km, int) or releve_km <= 0:
        return {'error': 'Le kilométrage doit être un entier positif.'}, 400

    if not source_releve or not isinstance(source_releve, str):
        return {'error': 'La source doit être une chaîne de caractères non vide.'}, 400

    # Vérifier que la voiture existe
    voiture = Voiture.query.filter_by(immat=immat).first()
    if not voiture:
        return {'error': 'Aucune voiture trouvée avec cette immatriculation.'}, 404

    # Créer un nouvel enregistrement dans la table RelevesKilometres
    new_releve = RelevesKilometres(
        immat=immat,
        releve_km=releve_km,
        date_releve=date.today(),  # Utiliser la date du jour
        source_releve=source_releve
    )

    # Ajouter et valider la transaction
    db.session.add(new_releve)
    db.session.commit()

    # Retourner le relevé créé
    return new_releve.to_dict(), 201

#recuperer les defauts d'un voiture
def get_defauts_veh(immat):
    defauts_veh = Defautsremarque.query.filter_by(immat=immat).all()
    return [defaut.to_dict() for defaut in defauts_veh]

#ajouter des defauts a un vehicule
def post_defaut_veh(immat, id_defaut, commentaire_libre):
     # Vérifier que la voiture existe
    voiture = Voiture.query.filter_by(immat=immat).first()
    if not voiture:
        return {'error': 'Aucune voiture trouvée avec cette immatriculation.'}, 404
    
    new_defaut = Defautsremarque(
        immat=immat,
        date_remarque=date.today(),
        id_categorie=id_defaut,
        commentaire_libre=commentaire_libre
    )
    db.session.add(new_defaut)
    db.session.commit()
    return {'message': 'Defaut ajouté avec succès'}, 201


def dernier_kilometrage(immat):
    dernier_releve = RelevesKilometres.query.filter_by(immat=immat).order_by(RelevesKilometres.releve_km.desc()).first()
    return dernier_releve.to_dict() if dernier_releve else None



#recupérer la distance entre deux endroits sur une map
def get_distance(origin, destination):

    try:
        # Appeler l'API Google Maps Distance Matrix
        response = gmaps.distance_matrix(origin, destination)

        # Extraire les données pertinentes (distance et durée)
        origin_address = response['origin_addresses'][0]
        destination_address = response['destination_addresses'][0]
        distance_km = response['rows'][0]['elements'][0]['distance']['text']
        duration = response['rows'][0]['elements'][0]['duration']['text']

        result = {
            "origin": origin_address,
            "destination": destination_address,
            "distance": distance_km,
            "duration": duration
        }
        # # Retourner les résultats
        return json.dumps(result)
    
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({"error": "Erreur lors du calcul de la distance"}), 500


# print(get_distance('Corte','Ajaccio'))


def get_co2_emission(distance_km):
    payload = {
        "vehicle_type": "Car-Type-LowerMedium",
        "fuel_type": "Petrol",
        "distance_value": distance_km,
        "distance_unit": "km"
        }
    co2headers = {
        "x-rapidapi-key": "730439462fmsh551cfcba5340416p1b46c1jsnfdb107cc22db",
        "x-rapidapi-host": "carbonsutra1.p.rapidapi.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer fQ98oU704xFvsnXcQLVDbpeCJHPglG1DcxiMLKfpeNEMGumlbzVf1lCI6ZBx"
    }

    response = requests.post(urlCO2E, data=payload, headers=co2headers)

    return response.json()

#print(get_co2_emission(100))