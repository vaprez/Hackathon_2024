import cv2
import easyocr
import matplotlib.pyplot as plt
import re  # Importer le module regex

# Chemin vers l'image
image_path = 'C:\Master2\Hackathon_2024\Code\API\images\plaque1.jpeg'
img = cv2.imread(image_path)

# Vérifiez si l'image est chargée
if img is None:
    print(f"Impossible de charger l'image : {image_path}")
    exit()

# Instance du lecteur
reader = easyocr.Reader(['en'], gpu=False)

# Détection de texte
text_results = reader.readtext(image_path)

# Expression régulière pour une plaque
# Exemple: Format français classique avec chiffres et lettres (XX-123-YY, GS-817-OP)
plate_regex = r'\b[A-Z]{2}-\d{3}-[A-Z]{2}\b'

# Parcourir les résultats et extraire uniquement les plaques
detected_plates = []
for result in text_results:
    bbox, detected_text, score = result
    print(f"Texte détecté : {detected_text} (score : {score})")

    # Chercher une correspondance avec la regex
    match = re.search(plate_regex, detected_text)
    if match:
        detected_plates.append(match.group())
        # Dessiner un rectangle autour de la plaque détectée
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(img, match.group(), top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Afficher les plaques détectées
print("Plaques détectées :", detected_plates)

# Afficher l'image annotée
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
