import argparse
import json
import requests
from datetime import datetime, timezone

def post_json_to_url(json_file, url, key):
    try:
        # Charge le contenu du fichier JSON
        with open(json_file, 'r') as file:
            data = json.load(file)

        # data = json.dumps(data, ident=4) # Convert le json.

        # Get time
        json_date = json_file.split("_")[0].split("/")[-1]
        data["metadata"] = {"name": json_file, "timestamp": json_date, "api_key": key}

        # Envoie le JSON à l'URL en tant que requête POST
        response = requests.post(url, json=data)

        # Vérifie la réponse HTTP
        if response.status_code == 200:
            print("Le JSON a été posté avec succès à l'URL :", url, " ", response.text)
        else:
            print(f"Erreur lors de la requête HTTP (code {response.status_code}): {response.text}")

    except Exception as e:
        print("Une erreur s'est produite :", str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Charge un fichier JSON et le poste vers une URL.")
    parser.add_argument("json_file", help="Chemin vers le fichier JSON à charger")
#     parser.add_argument("url", help="URL vers laquelle poster le JSON")
    parser.add_argument("key", help="Api key")

    url = "http://127.0.0.1:5000/push"
    args = parser.parse_args()
    post_json_to_url(args.json_file, url ,args.key)
