import cv2
import easyocr
import matplotlib.pyplot as plt
import re  # Importer le module regex


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

# Chemin vers l'image
image_path = r'C:\Master2\Hackathon_2024\Code\API\images\compteur1.jpeg'
img = cv2.imread(image_path)

# Vérifiez si l'image est chargée
if img is None:
    print(f"Impossible de charger l'image : {image_path}")
    exit()

# Instance du lecteur
reader = easyocr.Reader(['en'], gpu=True)

# Détection de texte
text_results = reader.readtext(image_path)

# Parcourir les résultats et extraire uniquement les textes contenant "km"
all_detected = []
for result in text_results:
    bbox, detected_text, score = result
    print(f"Texte détecté : {detected_text} (score : {score})")

    # Ajouter à la liste si le score est supérieur à 0.70
    if score > 0.70:
        all_detected.append(detected_text)

print(all_detected,"test1")
all_detected = supprimer_km(all_detected)
# Convertir les textes détectés en entiers
detected_km = convert_to_int_list(all_detected)
print(detected_km,"tes")

# Trouver le kilométrage le plus grand
if detected_km:
    max_km = max(detected_km)  # Trouver le maximum
    print(f"Kilométrage le plus grand : {max_km}km")
else:
    print("Aucun kilométrage détecté avec un score supérieur à 0.70.")

# Afficher l'image annotée
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
