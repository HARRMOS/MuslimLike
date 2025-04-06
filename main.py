from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Récupérer toutes les vidéos
@app.route("/getVideos", methods=["GET"])
def get_videos():
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="mh285989-001.eu.clouddb.ovh.net",
            port=35693,
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour interroger la base de données
        cursor = conn.cursor(dictionary=True)
        
        # Exécuter la requête SQL pour récupérer toutes les vidéos
        cursor.execute("SELECT * FROM `islamic_content`")
        results = cursor.fetchall()
        
        # Fermer la connexion
        conn.close()

        # Retourner les résultats sous forme de JSON
        return jsonify(results)
    
    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500

# Récupérer le nombre de likes d'une vidéo
@app.route("/video/<int:content_id>/likes", methods=["GET"])
def get_video_likes(content_id):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="mh285989-001.eu.clouddb.ovh.net",
            port=35693,
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour interroger la base de données
        cursor = conn.cursor(dictionary=True)
        
        # Exécuter la requête SQL pour obtenir le nombre de likes d'une vidéo
        cursor.execute("""
            SELECT COUNT(*) AS like_count 
            FROM `likes` 
            WHERE `content_id` = %s
        """, (content_id,))
        result = cursor.fetchone()
        
        # Fermer la connexion
        conn.close()

        # Vérifier si le résultat existe
        if result:
            return jsonify({"likes": result["like_count"]})
        else:
            return jsonify({"error": "Contenu non trouvé"}), 404
    
    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500

if __name__ == "__main__":
    # Lancer l'application Flask
    app.run(debug=True, host="0.0.0.0", port=6000)
