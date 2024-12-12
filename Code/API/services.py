# services.py
from models import Voiture, db
# from models import Typedefauts
from models import Defautsremarque
from datetime import date

def get_voitures():
    voitures = Voiture.query.all()
    return [voiture.to_dict() for voiture in voitures]

def get_voiture(immat):
    voiture = Voiture.query.get(immat)
    if voiture:
        return voiture.to_dict()
    
def get_defauts_veh(immat):
    defauts_veh = Defautsremarque.query.filter_by(immat=immat).all()
    return [defaut.to_dict() for defaut in defauts_veh]


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

    return {'message': 'Defaut ajouté avec succès'}
    



