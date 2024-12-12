# services.py
from models import db, Voiture, RelevesKilometres
from datetime import date

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


    return True
