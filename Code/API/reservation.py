@app.route('/destinations', methods=['GET'])
def destinations():
    return jsonify(get_destinations())

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
def post_reservations():
     data = request.json
     depart = data.get("depart")
     arrive = data.get("arrive")
     date_debut = data.get("date_debut")
     date_fin = data.get("date_fin")
     nb_personnes = data.get("nb_personnes")
     immatriculation = data.get("immat")
     nom_utilisateur = data.get("nom_utilisateur")

     # Validation des données
     if not (depart and arrive and date_debut and date_fin and nb_personnes and immatriculation and nom_utilisateur):
         return jsonify({"error": "Tous les champs sont requis."}), 400

     Resultats = post_reservations(depart,arrive,date_debut,date_fin,nb_personnes,immat,nom_utilisateur)

     return Resultats


def get_destinations():
    destinations = destination_possibles.query.all()
    return [destination.to_dict() for destination in destinations]

def search_reservations(depart,arrive,date_debut,date_fin,nb_personnes):
    distance = 20


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

