-- Voitures Table
CREATE TABLE Voitures (
    immat VARCHAR(20) PRIMARY KEY,
    modele VARCHAR(50) NOT NULL,
    propulsion VARCHAR(50) NOT NULL,
    nb_places INTEGER NOT NULL,
    autonomie_theorique INTEGER NOT NULL,
    taille_batterie INTEGER NULL,
    conso_kwh_100km DECIMAL(5,2) NULL,
    conso_lt_100km DECIMAL(5,2) NULL,
    site_rattachement VARCHAR(100) NOT NULL
);

-- Destinations Table
CREATE TABLE Destinations (
    id_destination SERIAL PRIMARY KEY,
    nom_destination VARCHAR(200) NOT NULL,
    lat DECIMAL(12,11) NOT NULL,
    lon DECIMAL(12,11) NOT NULL
);

-- RelevesKilometres Table
CREATE TABLE RelevesKilometres (
    id_releve SERIAL PRIMARY KEY,
    immat VARCHAR(20) NOT NULL,
    releve_km INTEGER NOT NULL,
    date_releve DATE NOT NULL,
    source_releve VARCHAR(100) NOT NULL,
    FOREIGN KEY (immat) REFERENCES Voitures(immat)
);

-- typeDefauts Table
CREATE TABLE typeDefauts (
    id_defaut SERIAL PRIMARY KEY,
    categorie VARCHAR(100) NOT NULL
);

-- DefautsRemarque Table
CREATE TABLE DefautsRemarque (
    id_releve SERIAL PRIMARY KEY,
    immat VARCHAR(20) NOT NULL,
    date_remarque DATE NOT NULL,
    id_categorie INTEGER NOT NULL,
    commentaire_libre TEXT,
    FOREIGN KEY (immat) REFERENCES Voitures(immat),
    FOREIGN KEY (id_categorie) REFERENCES typeDefauts(id_defaut)
);

-- PlanningReservation Table
CREATE TABLE PlanningReservation (
    id_res SERIAL PRIMARY KEY,
    immat VARCHAR(20) NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    nb_places_reserves INTEGER NOT NULL,
    nom_utilisateur VARCHAR(100) NOT NULL,
    FOREIGN KEY (immat) REFERENCES Voitures(immat)
);
