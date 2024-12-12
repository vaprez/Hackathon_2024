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
    id_defaut = db.Column(db.Integer, primary_key=True)
    categorie = db.Column(db.String(20), nullable=False)
    def to_dict(self):
        return {
            'id_defaut': self.id_defaut,
            'categorie': self.categorie,
        }
    



class Defautsremarque(db.Model):
    __tablename__ = 'defautsremarque' 
    id_releve = db.Column(db.Integer, primary_key=True)
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