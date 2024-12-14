# services.py
from models import db, Voiture, RelevesKilometres, Defautsremarque, Destination, PlanningReservation, Typedefauts
from datetime import date
from flask import jsonify
import googlemaps , json, requests, os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


GOOGLE_MAPS_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")
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

def get_typedefauts():
    defauts = Typedefauts.query.all()
    return [defaut.to_dict() for defaut in defauts]

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

def get_destinations():
    destinations = Destination.query.all()
    return [destination.to_dict() for destination in destinations]

def dernier_kilometrage(immat):
    dernier_releve = RelevesKilometres.query.filter_by(immat=immat).order_by(RelevesKilometres.releve_km.desc()).first()
    return dernier_releve.to_dict() if dernier_releve else None

def ajout_reservations(depart,arrivee,date_debut,date_fin,nb_personnes,immatriculation,nom_utilisateur):
    # Vérifier si le véhicule existe
    vehicule = Voiture.query.get(immatriculation)
    if not vehicule:
         return jsonify({"error": "Le véhicule avec cette immatriculation n'existe pas."}), 404

    # Ajouter la réservation dans la base de données
    nouvelle_reservation = PlanningReservation(
        depart = depart,
        arrivee = arrivee,
        immat=immatriculation,
        date_debut=date_debut,
        date_fin=date_fin,
        nb_places_reserves=nb_personnes,
        nom_utilisateur=nom_utilisateur
    )

    try:
        db.session.add(nouvelle_reservation)
        db.session.commit()
        return jsonify({"message": "Réservation ajoutée avec succès.", "reservation_id": nouvelle_reservation.id_res}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Une erreur est survenue lors de l'ajout de la réservation: {str(e)}"}), 500


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
            "distance": int(distance_km.replace(" km", "")),
            "duration": duration
        }
        # # Retourner les résultats
        return json.dumps(result)
    
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({"error": "Erreur lors du calcul de la distance"}), 500


def reservations_recherche(depart,arrivee,date_debut,date_fin,nb_personnes):
    destDepart = Destination.query.get(depart)
    destArrivee = Destination.query.get(arrivee)
    
    distances= get_distance(destDepart.nom_destination,destArrivee.nom_destination)
    distance = json.loads(distances)["distance"]

    reservations = PlanningReservation.query.filter(
    PlanningReservation.date_debut == date_debut,
    PlanningReservation.depart == depart,
    PlanningReservation.arrivee == arrivee).all()

    resultats_covoiturage = []
    for reservation in reservations:
        # Récupérer le véhicule associé
        voiture = Voiture.query.filter_by(immat=reservation.immat).first()
        if voiture:
            places_disponibles = voiture.nb_places - reservation.nb_places_reserves
            if int(places_disponibles) >= int(nb_personnes):
                # Ajouter la réservation valide aux résultats
                resultats_covoiturage.append({
                    "id_res": reservation.id_res,
                    "immat": reservation.immat,
                    "date_debut": reservation.date_debut.strftime("%d/%m/%Y"),
                    "date_fin": reservation.date_fin.strftime("%d/%m/%Y"),
                    "nb_places_disponibles": places_disponibles,
                    "nom_utilisateur": reservation.nom_utilisateur,
                    "depart" : reservation.depart,
                    "arrivee" : reservation.arrivee
                })

    # Filtrer les véhicules selon le nombre de places
    vehicules_disponibles = Voiture.query.filter(
        Voiture.nb_places > nb_personnes
    ).all()

     # Filtrer les véhicules électriques avec une autonomie suffisante
    vehicules_valides = []
    for vehicule in vehicules_disponibles:
         if vehicule.propulsion.lower() == "électrique":
             # Vérifier si l'autonomie est suffisante
             if vehicule.autonomie_theorique >= (distance * 2):
                 vehicules_valides.append({
                     "immat": vehicule.immat,
                     "modele": vehicule.modele,
                     "propulsion": vehicule.propulsion,
                     "nb_places": vehicule.nb_places,
                     "autonomie_theorique": vehicule.autonomie_theorique
                 })
         else:
             # Ajouter directement les véhicules thermiques
             vehicules_valides.append({
                 "immat": vehicule.immat,
                 "modele": vehicule.modele,
                 "propulsion": vehicule.propulsion,
                 "nb_places": vehicule.nb_places,
                 "autonomie_theorique": vehicule.autonomie_theorique
             })

    # Retourner les résultats
    if resultats_covoiturage and vehicules_valides :
        return jsonify({"reservations_covoiturage": resultats_covoiturage},{"vehicules_disponibles": vehicules_valides})
    else:
        return jsonify([])


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
