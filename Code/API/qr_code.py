from flask import Flask

app = Flask(__name__)

@app.route("/qr-code", methods=["POST"])
def qr_code_reader():
    # Chemin de l'image dans le dossier "api"
    img_path = os.path.join("images", "qr_image.png")

    if not os.path.exists(img_path):
        return jsonify({"error": "L'image spécifiée n'existe pas."}), 400

    with open(img_path, "rb") as img_file:
        url = "http://api.qrserver.com/v1/read-qr-code/"

        files = {
            'file': ('file', img_file)
        }

        try:
            res = requests.post(url, files=files)

            if res.status_code == 200:
                data = res.json()
                return jsonify(data), 200
            else:
                return jsonify({"error": "Échec de l'exécution de l'API QR.", "status_code": res.status_code}), res.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500