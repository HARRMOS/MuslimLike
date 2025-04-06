from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/content/<int:content_id>/likes", methods=["GET"])
def get_likes(content_id):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="mh285989-001.eu.clouddb.ovh.net",
            port=35693,  # Spécifier le port ici
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour interroger la base de données
        cursor = conn.cursor(dictionary=True)

        # Exécuter la requête pour obtenir le nombre de likes pour un contenu donné
        cursor.execute(
            "SELECT COUNT(*) AS like_count FROM likes WHERE content_id = %s",
            (content_id,)
        )
        result = cursor.fetchone()

        # Fermer la connexion
        conn.close()

        # Vérifier si le contenu existe
        if result:
            return jsonify({"likes": result["like_count"]})
        else:
            return jsonify({"error": "Contenu non trouvé"}), 404

    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500


@app.route("/content/<int:content_id>/like", methods=["POST"])
def like_content(content_id):
    try:
        # Récupérer l'ID de l'utilisateur dans le corps de la requête
        user_id = request.json.get("userId")

        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="mh285989-001.eu.clouddb.ovh.net",
            port=35693,  # Spécifier le port ici
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour interroger la base de données
        cursor = conn.cursor(dictionary=True)

        # Vérifier si l'utilisateur a déjà liké
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = %s AND content_id = %s) AS has_liked",
            (user_id, content_id)
        )
        result = cursor.fetchone()

        if result and result["has_liked"]:
            # Supprimer le like
            cursor.execute(
                "DELETE FROM likes WHERE user_id = %s AND content_id = %s",
                (user_id, content_id)
            )
            conn.commit()
            return jsonify({"liked": False})

        else:
            # Ajouter le like
            cursor.execute(
                "INSERT INTO likes (user_id, content_id) VALUES (%s, %s)",
                (user_id, content_id)
            )
            conn.commit()
            return jsonify({"liked": True})

        # Fermer la connexion
        conn.close()

    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500


if __name__ == "__main__":
    # Lancer l'application Flask
    app.run(debug=True, host="0.0.0.0", port=6000)
