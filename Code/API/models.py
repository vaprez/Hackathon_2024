# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicule(db.Model):
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
