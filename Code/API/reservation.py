
@app.route('/search_reservations',methods=['POST'])
def search_reservations():
    data = request.get_json()
    depart = data.get("depart")
    arrive = data.get("arrive")
    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    nb_personnes = data.get("nb_personnes")

    if nb_personnes is None or distance is None or depart is None or arrive is None or date_debut is None or date_fin is None:
                return jsonify({"error": "Veuillez fournir 'nb_personnes' et 'distance'."}), 400

    resultats = search_reservations(depart,arrive,debut,fin,nb_personnes)

    return resultats

@app.route('/reservations', methods=['POST'])

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



def get_destinations():
    destinations = destination_possibles.query.all()
    return [destination.to_dict() for destination in destinations]

def search_reservations(depart,arrive,date_debut,date_fin,nb_personnes):
    _,_,distance,_ = get_distance(depart,arrive)


    reservations = Planning_reservations.query.filter(
    Planning_reservations.date_debut == date_debut,
    Planning_reservations.depart == depart,
    Planning_reservations.arrive == arrive).all()

    resultats_covoiturage = []
    for reservation in reservations:
        # Récupérer le véhicule associé
        voiture = Voiture.query.filter_by(immat=reservation.immat).first()
        if voiture:
            places_disponibles = voiture.nb_places - reservation.nb_place_reserves
            if places_disponibles >= nb_personnes:
                # Ajouter la réservation valide aux résultats
                resultats_covoiturage.append({
                    "id_res": reservation.id_res,
                    "immat": reservation.immat,
                    "date_debut": reservation.date_debut.strftime("%d/%m/%Y"),
                    "date_fin": reservation.date_fin.strftime("%d/%m/%Y"),
                    "nb_places_disponibles": places_disponibles,
                    "nom_utilisateur": reservation.nom_utilisateur,
                    "depart" : reservation.depart,
                    "arrive" : reservation.arrive
                })

    # Filtrer les véhicules selon le nombre de places
    vehicules_disponibles = Voiture.query.filter(
        Voiture.nb_places >= nb_personnes
    ).all()

    # Filtrer les véhicules électriques avec une autonomie suffisante
    vehicules_valides = []
    for vehicule in vehicules_disponibles:
        if vehicule.propulsion.lower() == "électrique":
            # Vérifier si l'autonomie est suffisante
            if vehicule.autonomie_theorique >= (distance * 2):
                vehicules_valides.append({
                    "id_vehicule": vehicule.id_vehicule,
                    "immat": vehicule.immat,
                    "modele": vehicule.modele,
                    "propulsion": vehicule.propulsion,
                    "nb_places": vehicule.nb_places,
                    "autonomie_theorique": vehicule.autonomie_theorique
                })
        else:
            # Ajouter directement les véhicules thermiques
            vehicules_valides.append({
                "id_vehicule": vehicule.id_vehicule,
                "immat": vehicule.immat,
                "modele": vehicule.modele,
                "propulsion": vehicule.propulsion,
                "nb_places": vehicule.nb_places,
                "autonomie_theorique": vehicule.autonomie_theorique
            })

    # Retourner les résultats
    if resultats:
        return jsonify({"reservations_covoiturage": resultats_covoiturage},{"vehicules_disponibles": vehicules_valides})
    else:
        return jsonify({"message": "Aucune réservation disponible pour ces critères."})


def post_reservations(depart,arrive,date_debut,date_fin,nb_personnes,immat,nom_utilisateur):
    # Vérifier si le véhicule existe
    vehicule = Voiture.query.filter_by(immat=immatriculation).first()
    if not vehicule:
         return jsonify({"error": "Le véhicule avec cette immatriculation n'existe pas."}), 404

    # Ajouter la réservation dans la base de données
    nouvelle_reservation = PlanningReservations(
        depart = depart,
        arrive = arrive,
        immat=immatriculation,
        date_debut=date_debut,
        date_fin=date_fin,
        nb_place_reserves=nb_personnes,
        nom_utilisateur=nom_utilisateur
    )

    try:
        session.add(nouvelle_reservation)
        session.commit()
        return jsonify({"message": "Réservation ajoutée avec succès.", "reservation_id": nouvelle_reservation.id_res}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": f"Une erreur est survenue lors de l'ajout de la réservation: {str(e)}"}), 500



