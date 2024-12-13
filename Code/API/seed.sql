INSERT INTO
    typedefauts (categorie)
VALUES ('essuie glaces'),
    ('vitres'),
    ('pneus'),
    ('mécanique'),
    ('éclairage'),
    ('manque equipement'),
    ('autonomie'),
    ('autre');

INSERT INTO
    voitures (
        immat,
        modele,
        propulsion,
        nb_places,
        autonomie_theorique,
        taille_batterie,
        conso_kwh_100km,
        conso_lt_100km,
        site_rattachement
    )
VALUES (
        'AB123CD',
        'Renault Zoe',
        'Électrique',
        5,
        395,
        52,
        15.4,
        0.0,
        'Paris'
    ),
    (
        'EF456GH',
        'Peugeot 208',
        'Essence',
        5,
        600,
        0,
        0.0,
        4.8,
        'Lyon'
    ),
    (
        'IJ789KL',
        'Tesla Model 3',
        'Électrique',
        5,
        491,
        75,
        16.6,
        0.0,
        'Marseille'
    ),
    (
        'MN012OP',
        'Toyota Prius',
        'Hybride',
        5,
        1000,
        8,
        5.0,
        3.5,
        'Nice'
    ),
    (
        'QR345ST',
        'Volkswagen ID.4',
        'Électrique',
        5,
        522,
        77,
        17.2,
        0.0,
        'Bordeaux'
    ),
    (
        'UV678WX',
        'Citroën C5 Aircross',
        'Essence',
        5,
        700,
        0,
        0.0,
        6.2,
        'Nantes'
    ),
    (
        'YZ901AB',
        'Nissan Leaf',
        'Électrique',
        5,
        385,
        40,
        14.7,
        0.0,
        'Strasbourg'
    ),
    (
        'CD234EF',
        'Hyundai Ioniq 5',
        'Électrique',
        5,
        481,
        58,
        16.9,
        0.0,
        'Toulouse'
    ),
    (
        'GH567IJ',
        'Ford Kuga',
        'Hybride',
        5,
        800,
        10,
        6.0,
        5.6,
        'Lille'
    ),
    (
        'KL890MN',
        'BMW i3',
        'Électrique',
        4,
        310,
        42,
        13.1,
        0.0,
        'Rennes'
    );

INSERT INTO
    defautsremarque (
        immat,
        date_remarque,
        id_categorie,
        commentaire_libre
    )
VALUES (
        'AB123CD',
        '12-12-2024',
        6,
        ' il est cassé'
    ),
    (
        'AB123CD',
        '12-12-2024',
        5,
        ' il est cassé'
    ),
    (
        'AB123CD',
        '12-12-2024',
        3,
        ' il est cassé'
    ),
    (
        'MN012OP',
        '12-12-2024',
        1,
        ' il est cassé'
    ),
    (
        'CD234EF',
        '12-12-2024',
        7,
        ' il est cassé'
    )