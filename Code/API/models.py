# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Voiture(db.Model):
    __tablename__ = 'voitures'  # Nom de la table dans la base de données

    immat = db.Column(db.String(20), primary_key=True)
    modele = db.Column(db.String(50), nullable=False)
    propulsion = db.Column(db.String(50), nullable=False)
    nb_places = db.Column(db.Integer, nullable=False)
    autonomie_theorique = db.Column(db.Integer, nullable=False)
    taille_batterie = db.Column(db.Integer, nullable=True)
    conso_kwh_100km = db.Column(db.Numeric(5, 2), nullable=True)
    conso_lt_100km = db.Column(db.Numeric(5, 2), nullable=True)
    site_rattachement = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'immat': self.immat,
            'modele': self.modele,
            'propulsion': self.propulsion,
            'nb_places': self.nb_places,
            'autonomie_theorique': self.autonomie_theorique,
            'taille_batterie': self.taille_batterie,
            'conso_kwh_100km': float(self.conso_kwh_100km) if self.conso_kwh_100km else None,
            'conso_lt_100km': float(self.conso_lt_100km) if self.conso_lt_100km else None,
            'site_rattachement': self.site_rattachement
        }

class RelevesKilometres(db.Model):
    __tablename__ = 'releveskilometres'

    id_releve = db.Column(db.Integer, primary_key=True, autoincrement=True)
    immat = db.Column(db.String(20), db.ForeignKey('voitures.immat'), nullable=False)
    releve_km = db.Column(db.Integer, nullable=False)
    date_releve = db.Column(db.Date, nullable=False)
    source_releve = db.Column(db.String(100), nullable=False)



    def to_dict(self):
        return {
            'id_releve': self.id_releve,
            'immat': self.immat,
            'releve_km': self.releve_km,
            'date_releve': self.date_releve.isoformat(),  # Convertir la date en format ISO
            'source_releve': self.source_releve
        }


class Typedefauts(db.Model):
    __tablename__ = 'typedefauts' 
    id_defaut = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categorie = db.Column(db.String(20), nullable=False)
    def to_dict(self):
        return {
            'id_defaut': self.id_defaut,
            'categorie': self.categorie,
        }
    
class Destination(db.Model):
    __tablename__ = 'destinations'  # Nom de la table dans la base de données

    id_destination = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrément
    nom_destination = db.Column(db.String(200), nullable=False)
    lat = db.Column(db.Numeric(12, 11), nullable=False)
    lon = db.Column(db.Numeric(12, 11), nullable=False)

    def to_dict(self):
        return {
            'id_destination': self.id_destination,
            'nom_destination': self.nom_destination,
            'lat': float(self.lat),  # Convertir en float pour une meilleure lisibilité
            'lon': float(self.lon)   # Convertir en float pour une meilleure lisibilité
        }

class Defautsremarque(db.Model):
    __tablename__ = 'defautsremarque' 
    id_releve = db.Column(db.Integer, primary_key=True, autoincrement=True)
    immat = db.Column(db.String(20), nullable=False)
    date_remarque = db.Column(db.Date, nullable=False)
    id_categorie = db.Column(db.Integer, nullable=False)
    commentaire_libre = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        defaut = Typedefauts.query.get(self.id_categorie)
        return {
            'id_releve': self.id_releve,
            'immat': self.immat,
            'date_remarque': self.date_remarque,
            'id_categorie': self.id_categorie,
            'commentaire_libre': self.commentaire_libre,
            'categorie': defaut.categorie if defaut else None
        }

class PlanningReservation(db.Model):
    __tablename__ = 'planningreservation'  # Nom de la table dans la base de données

    id_res = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrément
    immat = db.Column(db.String(20), db.ForeignKey('voitures.immat'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    nb_places_reserves = db.Column(db.Integer, nullable=False)
    nom_utilisateur = db.Column(db.String(100), nullable=False)
    depart = db.Column(db.Integer, db.ForeignKey('destinations.id_destination'), nullable=False)  # Nouvelle colonne
    arrivee = db.Column(db.Integer, db.ForeignKey('destinations.id_destination'), nullable=False)  # Nouvelle colonne

    # Relations avec les tables Voitures et Destinations
    voiture = db.relationship('Voiture', foreign_keys=[immat])
    destination_depart = db.relationship('Destination', foreign_keys=[depart])
    destination_arrivee = db.relationship('Destination', foreign_keys=[arrivee])

    def to_dict(self):
        return {
            'id_res': self.id_res,
            'immat': self.immat,
            'date_debut': self.date_debut.isoformat(),
            'date_fin': self.date_fin.isoformat(),
            'nb_places_reserves': self.nb_places_reserves,
            'nom_utilisateur': self.nom_utilisateur,
            'depart': self.depart,
            'arrivee': self.arrivee
        }
