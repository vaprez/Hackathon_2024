# services.py
from models import Vehicule

def get_vehicules():
    vehicules = Vehicule.query.all()
    return [vehicule.to_dict() for vehicule in vehicules]

def get_vehicule(immat):
    vehicule = Vehicule.query.get(immat)
    if vehicule:
        return vehicule.to_dict()

