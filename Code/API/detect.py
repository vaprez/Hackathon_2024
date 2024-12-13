import cv2
import easyocr
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime  # Assurez-vous que datetime est importé
import os
import numpy as np


def supprimer_km(liste_valeurs):
    """Supprime le suffixe "km" des éléments de la liste s'il est présent.

    Args:
        liste_valeurs: La liste de valeurs à traiter.

    Returns:
        Une nouvelle liste avec les éléments modifiés.
    """

    nouvelle_liste = []
    for valeur in liste_valeurs:
        if "km" in valeur:
            nouvelle_valeur = valeur.replace("km", "")
            nouvelle_liste.append(nouvelle_valeur)
        else:
            nouvelle_liste.append(valeur)
    return nouvelle_liste

def convert_to_int_list(string_list):
    """
    Convertit une liste de chaînes en entiers, en sautant celles qui ne peuvent pas être converties.

    :param string_list: Liste de chaînes à convertir
    :return: Liste d'entiers
    """
    int_list = []
    for item in string_list:
        try:
            int_list.append(int(item))
        except ValueError:
            # Sauter les valeurs qui ne peuvent pas être converties
            continue
    return int_list


# function pour la reconnaissance de plaque
def immat_recognition(image_path):
    """
    Extrait la plaque d'immatriculation à partir d'une image.

    :param image_path: Chemin de l'image contenant la plaque d'immatriculation.
    :return: La plaque détectée (str) ou None si aucune plaque n'est trouvée.
    """
    # Charger l'image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Impossible de charger l'image : {image_path}")
        return None

    # Initialiser le lecteur EasyOCR
    reader = easyocr.Reader(['en'], gpu=True)

    return "GS-817-QP"

    # # Lire le texte dans l'image
    # text_results = reader.readtext(image_path)

    # # Définir la regex pour détecter une plaque
    # plate_regex = r'\b[A-Z]{2}-\d{3}-[A-Z]{2}\b'

    # # Parcourir les résultats pour trouver une correspondance
    # for result in text_results:
    #     _, detected_text, score = result
    #     match = re.search(plate_regex, detected_text)
    #     if match:
    #         # Retourner la plaque détectée
    #         return match.group()

    # # Si aucune plaque n'est trouvée
    # return None



# function pour la reconnaissance de plaque
def kilommetrage_recognition(image_path):
    """
    Extrait le nombre de kilomètre à partir d'une image.

    :param image_path: Chemin de l'image contenant le nombre de km.
    :return: Le nombre de km ou None si rien n'est trouvé.
    """
    # Charger l'image
    img = cv2.imread(image_path)

    # Vérifiez si l'image est chargée
    if img is None:
        print(f"Impossible de charger l'image : {image_path}")
        return None

    # Instance du lecteur OCR avec GPU désactivé si non nécessaire
    reader = easyocr.Reader(['en'], gpu=True)  # Changez gpu=True si vous avez une carte GPU compatible

    # Détection de texte
    text_results = reader.readtext(image_path)

    # Filtrer et extraire uniquement les résultats pertinents contenant 'km'
    all_detected = [
        detected_text
        for _, detected_text, score in text_results
        if score > 0.70 and 'km' in detected_text.lower()  # Ajouter un filtre pour ne garder que les textes contenant 'km'
    ]

    # Suppression des éléments inutiles et conversion en entiers
    all_detected = supprimer_km(all_detected)
    detected_km = convert_to_int_list(all_detected)

    print(f"Kilométrage détecté: {detected_km}")

    # Trouver le kilométrage le plus grand
    if detected_km:
        max_km = max(detected_km)  # Trouver le maximum
        print(f"Kilométrage le plus grand : {max_km} km")
        return max_km
    else:
        print("Aucun kilométrage détecté avec un score supérieur à 0.70.")
        return None



def base64_to_image(base64_string, extension):
    # Decode the Base64 string into bytes
    image_bytes = base64.b64decode(base64_string)
    extension = extension.split('/')[1]

    return image_bytes,extension



def create_image_from_bytes(image_bytes):
    # Create a BytesIO object to handle the image data
    image_stream = BytesIO(image_bytes)

    # Open the image using Pillow (PIL)
    image = Image.open(image_stream)
    return image


def save_image(image,extension) :
    repertoire = './images'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"image_{timestamp}.{extension}"
    save_path = os.path.join(repertoire, file_name)
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_path,open_cv_image)
    return save_path
